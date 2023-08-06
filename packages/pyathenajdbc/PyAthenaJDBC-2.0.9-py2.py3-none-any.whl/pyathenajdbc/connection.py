# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import os

import jpype
from future.utils import iteritems

from pyathenajdbc import (
    ATHENA_CONNECTION_STRING,
    ATHENA_DRIVER_CLASS_NAME,
    ATHENA_JAR,
    LOG4J_PROPERTIES,
)
from pyathenajdbc.converter import JDBCTypeConverter
from pyathenajdbc.cursor import Cursor
from pyathenajdbc.error import NotSupportedError, ProgrammingError
from pyathenajdbc.formatter import ParameterFormatter
from pyathenajdbc.util import attach_thread_to_jvm, synchronized

_logger = logging.getLogger(__name__)


class Connection(object):

    _ENV_S3_STAGING_DIR = "AWS_ATHENA_S3_STAGING_DIR"
    _ENV_WORK_GROUP = "AWS_ATHENA_WORK_GROUP"
    _BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(
        self,
        s3_staging_dir=None,
        access_key=None,
        secret_key=None,
        region_name=None,
        schema_name="default",
        profile_name=None,
        credential_file=None,
        jvm_path=None,
        jvm_options=None,
        converter=None,
        formatter=None,
        driver_path=None,
        log4j_conf=None,
        work_group=None,
        **driver_kwargs
    ):
        self.s3_staging_dir = (
            s3_staging_dir
            if s3_staging_dir
            else os.getenv(self._ENV_S3_STAGING_DIR, None)
        )
        self.work_group = (
            work_group if work_group else os.getenv(self._ENV_WORK_GROUP, None)
        )
        self.schema_name = schema_name

        assert schema_name, "Required argument `schema_name` not found."
        assert (
            self.s3_staging_dir or self.work_group
        ), "Required argument `s3_staging_dir` or `work_group` not found."

        if credential_file:
            self.access_key = None
            self.secret_key = None
            self.token = None
            self.profile_name = None
            self.credential_file = credential_file
            assert (
                self.credential_file
            ), "Required argument `credential_file` not found."
            self.region_name = region_name
            assert self.region_name, "Required argument `region_name` not found."
        else:
            import botocore.session

            session = botocore.session.get_session()
            if access_key and secret_key:
                session.set_credentials(access_key, secret_key)
            if profile_name:
                session.set_config_variable("profile", profile_name)
            if region_name:
                session.set_config_variable("region", region_name)
            credentials = session.get_credentials()
            self.access_key = credentials.access_key
            assert self.access_key, "Required argument `access_key` not found."
            self.secret_key = credentials.secret_key
            assert self.secret_key, "Required argument `secret_key` not found."
            self.token = credentials.token
            self.profile_name = session.profile
            self.credential_file = None
            self.region_name = session.get_config_variable("region")
            assert self.region_name, "Required argument `region_name` not found."

        self._start_jvm(jvm_path, jvm_options, driver_path, log4j_conf)

        self._driver_kwargs = driver_kwargs
        props = self._build_driver_args()
        jpype.JClass(ATHENA_DRIVER_CLASS_NAME)
        self._jdbc_conn = jpype.java.sql.DriverManager.getConnection(
            ATHENA_CONNECTION_STRING.format(
                region=self.region_name, schema=schema_name
            ),
            props,
        )

        self._converter = converter if converter else JDBCTypeConverter()
        self._formatter = formatter if formatter else ParameterFormatter()

    @classmethod
    @synchronized
    def _start_jvm(cls, jvm_path, jvm_options, driver_path, log4j_conf):
        if jvm_path is None:
            jvm_path = jpype.get_default_jvm_path()
        if driver_path is None:
            driver_path = os.path.join(cls._BASE_PATH, ATHENA_JAR)
        if log4j_conf is None:
            log4j_conf = os.path.join(cls._BASE_PATH, LOG4J_PROPERTIES)
        if not jpype.isJVMStarted():
            _logger.debug("JVM path: %s", jvm_path)
            args = [
                "-server",
                "-Djava.class.path={0}".format(driver_path),
                "-Dlog4j.configuration=file:{0}".format(log4j_conf),
            ]
            if jvm_options:
                args.extend(jvm_options)
            _logger.debug("JVM args: %s", args)
            if jpype.__version__.startswith("0.6"):
                jpype.startJVM(jvm_path, *args)
            else:
                jpype.startJVM(
                    jvm_path, *args, ignoreUnrecognized=True, convertStrings=True
                )
            cls.class_loader = (
                jpype.java.lang.Thread.currentThread().getContextClassLoader()
            )
        if not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
            if not cls.class_loader:
                cls.class_loader = (
                    jpype.java.lang.Thread.currentThread().getContextClassLoader()
                )
            class_loader = jpype.java.net.URLClassLoader.newInstance(
                [jpype.java.net.URL("jar:file:{0}!/".format(driver_path))],
                cls.class_loader,
            )
            jpype.java.lang.Thread.currentThread().setContextClassLoader(class_loader)

    def _build_driver_args(self):
        props = jpype.java.util.Properties()
        if self.credential_file:
            props.setProperty(
                "AwsCredentialsProviderClass",
                "com.simba.athena.amazonaws.auth.PropertiesFileCredentialsProvider",
            )
            props.setProperty(
                "aws_credentials_provider_arguments", self.credential_file
            )
        elif self.profile_name:
            props.setProperty(
                "AwsCredentialsProviderClass",
                "com.simba.athena.amazonaws.auth.profile.ProfileCredentialsProvider",
            )
            props.setProperty("aws_credentials_provider_arguments", self.profile_name)
        elif self.token:
            props.setProperty(
                "AwsCredentialsProviderClass",
                "com.simba.athena.amazonaws.auth.DefaultAWSCredentialsProviderChain",
            )
        else:
            props.setProperty("UID", self.access_key)
            props.setProperty("PWD", self.secret_key)
        props.setProperty("Schema", self.schema_name)
        if self.s3_staging_dir:
            props.setProperty("S3OutputLocation", self.s3_staging_dir)
        if self.work_group:
            props.setProperty("Workgroup", self.work_group)
        for k, v in iteritems(self._driver_kwargs):
            if k and v:
                props.setProperty(k, v)
        return props

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @attach_thread_to_jvm
    def cursor(self):
        if self.is_closed:
            raise ProgrammingError("Connection is closed.")
        return Cursor(self._jdbc_conn, self._converter, self._formatter)

    @attach_thread_to_jvm
    @synchronized
    def close(self):
        if not self.is_closed:
            self._jdbc_conn.close()
            self._jdbc_conn = None

    @property
    @attach_thread_to_jvm
    def is_closed(self):
        return self._jdbc_conn is None or self._jdbc_conn.isClosed()

    def commit(self):
        """Athena JDBC connection is only supported for auto-commit mode."""
        pass

    def rollback(self):
        raise NotSupportedError(
            "Athena JDBC connection is only supported for auto-commit mode."
        )
