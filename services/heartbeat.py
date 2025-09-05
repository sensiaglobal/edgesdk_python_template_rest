"""heartbeat.py

Thread class to manage application heartbeat and operation status.
"""

import os
import time
import logging
import threading
from http import HTTPStatus

# Third party
import requests

# Local
from api import RestAPI
from config import AppConfig, ExitCode
from services import Provisioning

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


class Heartbeat(threading.Thread):
    """Application heartbeat thread.
    
    This thread constantly pings the HCC2 Rest Server and updates the application heartbeat.
    """
    last_heartbeat = False

    def __init__(self):
        """Initialize the provisioning thread."""
        super().__init__()
        self.heartbeat_task_rest = RestAPI(version=1)
        self.failed_attempts = 0
        AppConfig.running(set_state=True)

    def run(self):
        while True:
            try:
                heartbeat_response = self.heartbeat_task_rest.heartbeat_app(
                    AppConfig.app_func_name,
                    is_up=Provisioning.is_provisioned
                )

                if heartbeat_response.ok:
                    hcc2_logger.debug(f"Heartbeat emitted. Provisioning Status : {Provisioning.is_provisioned}")
                    self.failed_attempts = 0
                    Heartbeat.last_heartbeat = True
                    AppConfig.running(set_state=True)
                    time.sleep(AppConfig.heartbeat_interval)

                elif heartbeat_response.status_code == HTTPStatus.NOT_FOUND:
                    hcc2_logger.critical(f"Heartbeat failed: Application {AppConfig.app_func_name} is not registered.")
                    AppConfig.running(set_state=False)
                    os._exit(ExitCode.REGISTRATION_NO_LONGER_VALID)

            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                hcc2_logger.error(f"Heartbeat attempt {self.failed_attempts+1} failed.")
                self.failed_attempts += 1
                if self.failed_attempts >= 10:
                    hcc2_logger.critical("Heartbeat has failed 10 times. Shutting down application.")
                    Heartbeat.last_heartbeat = False
                    AppConfig.running(set_state=False)
                    os._exit(ExitCode.REST_SERVER_NOT_FOUND)
                time.sleep(1)
