"""config.py

Load and process the config.json file."""

import os
import json
import socket
import logging
import threading


# AppConfig is a read only data class with minimal app control.
# pylint: disable=R0903

class AppConfig:
    """Python application source code config class."""

    config_file = "config.json"

    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

    # App
    app_name = config["app"]["name"]
    app_func_name = config["app"]["function_name"]
    app_ver_major = config["app"]["version"]["major"]
    app_ver_minor = config["app"]["version"]["minor"]
    app_ver_micro = config["app"]["version"]["micro"]
    app_version = f'v{app_ver_major}.{app_ver_minor}.{app_ver_micro}'
    app_log_level = os.getenv('LOG_LEVEL', config["app"]["log_level"])
    _app_running = threading.Event()

    # Logging
    hcc2_logger = logging.getLogger(app_func_name)
    hcc2_logger.propagate = False

    # App Registration
    app_reg_static_en = config["registration"]["static_enabled"]
    app_reg_dynamic_general_en = config["registration"]["dynamic_general_enable"]
    app_reg_dynamic_config_en = config["registration"]["dynamic_config_enable"]
    app_reg_premade_targz = config["registration"]["targz"]

    # Heartbeat
    heartbeat_interval = config["heartbeat"]["interval"]

    # Provisioning
    provisioning_complex = config["provisioning"]["complex"]
    provisioning_exit_if_failed = False
    provisioning_poll = 1

    # Network
    rest_ip = None
    app_ip = None

    # Rest API
    rest_port = config["rest_api"]["port"]
    rest_version = config["rest_api"]["version"]
    rest_verify_ssl = False

    def __setattr__(self, name, value):
        raise AttributeError("Configuration class is read-only.")

    @classmethod
    def running(cls, set_state=None):
        """Is application currently running."""
        if set_state is not None:
            if set_state:
                cls._app_running.set()
            else:
                cls._app_running.clear()

        return cls._app_running.is_set()

    @classmethod
    def resolve_ips(cls):
        """Attempt to get this applications and the HCC2 rest server IP addresses."""
        try:
            # Attempt to resolve the REST server IP on edgenet
            cls.rest_ip = socket.gethostbyname_ex('hcc2RestServer_0')[2][0]

        except (socket.gaierror, IndexError):
            cls.rest_ip = cls.config["network"]["rest_ip_override"]

        try:
            # Attempt to resolve this apps IP on edgenet
            cls.app_ip = socket.gethostbyname_ex(cls.app_func_name)[2][0]

        except (socket.gaierror, IndexError):
            cls.app_ip = cls.config["network"]["app_ip_override"]


class ExitCode():
    """Python application source code exit codes."""

    SUCCESS = 0
    REGISTRATION_FAILED = 1
    AUTHENTICATION_FAILED = 2
    PROVISIONING_FAILED = 3
    SERVER_ERROR = 4
    INVALID_INPUT = 5
    UNEXPECTED_ERROR = 6
    REGISTRATION_DISABLED = 7
    REGISTRATION_NO_LONGER_VALID = 8
    REST_SERVER_NOT_FOUND = 20
    REST_SERVER_PORT_NOT_OPEN = 21
