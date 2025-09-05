"""app.py

# Copyright (c) 2025 Sensia Global
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

=============================================================================
                      Sample HCC2 Python Application
=============================================================================
Description:
This is template code for a python HCC2 user application. This application can,

   - Handle complex or simple provisioning.
   - Register a premade TAR.GZ with or without additional dynamic data points.
   - Manage the setup and retrieval of HCC2 message subscription data.


=============================================================================
"""

import os
import sys
import time
import logging
import threading
from abc import ABC, abstractmethod

# Local
from api import RestAPI
from config import AppConfig, ExitCode
from services import Provisioning, PostValidConfig, Subscriptions, registration, Heartbeat
from api.hcc2_rest_schema import (
    TagMetadata, TagUnityUI, GeneralDataPoint, ConfigDataPoint,
    SimpleMessage, ComplexMessage, DataPoint
)
from api.hcc2_rest_enums import (
    TagDataType, TagSubClass, UnitType, BuiltInEnum
)
from utils import info_banner, DataPoints

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


# =============================================================================
#                         Add Dynamic General Data Points
# =============================================================================


# =============================================================================
#                          Add Dynamic Config Data Points
# =============================================================================


# =============================================================================
#                           Threaded Task Defintions
# =============================================================================

class Task(threading.Thread, ABC):
    """Base class for a threaded task."""

    def __init__(self, name, run_unprovisioned=False):
        super().__init__()
        self.name = name
        self.stop_task_event = threading.Event()
        self._state = None
        self.daemon = True
        self.run_without_provisioning = run_unprovisioned

        # Delays
        self.fail_state_timeout = 10
        self.provisionin_timeout = 5

    def run(self):
        """Run the task."""
        hcc2_logger.info(f"Task {self.name} starting")
        while not self.stop_task_event.is_set() and AppConfig.running():

            # Run if provisioned
            if Provisioning.is_provisioned or self.run_without_provisioning:
                try:
                    self.state('running')
                    self.execute()

                except Exception as e:
                    self.state('failed')
                    hcc2_logger.error(f"Task {self.name} failed due to {e}")
                    time.sleep(self.fail_state_timeout)  # Fail state timeout

            else:
                self.state('unprovisioned')

        hcc2_logger.debug(f"Task {self.name} stopping")
        self.state('stopped')

    def state(self, state : str):
        """Set task state."""
        if state != self._state:
            hcc2_logger.info(f"Task {self.name} : {state}")
        self._state = state

    def stop(self):
        """Stop the task."""
        self.stop_task_event.set()

    @abstractmethod
    def execute(self):
        """Task loop operation. Must override."""
        pass


class Task1(Task):
    """Thread task 1."""

    def __init__(self, run_unprovisioned=True):
        super().__init__("Task 1", run_unprovisioned)
        self.api = RestAPI()

    def execute(self):
        """Thread task 1 loop function"""

        # Add task logic here.
        time.sleep(1)


class Task2(Task):
    """Thread task 2."""

    def __init__(self, run_unprovisioned=False):
        super().__init__("Task 2", run_unprovisioned)

    def execute(self):
        """Thread task 2 loop function"""

        # Add task logic here.
        time.sleep(1)


# =============================================================================
#                           Provisioning Validation
# =============================================================================

def complex_provisioning_validation(self : Provisioning) -> bool:
    """Custom provisioning validation logic if complex provisioning is enabled.

    Add your validation logic for the values of CONFIG DATAPOINTS ONLY.
    
    If simple provisioning is enabled this function will be skipped and any incoming 
    pre-valid configuration values will be automatically accepted."""

    pvc = self.pre_valid_config

    # Add validations for pre-valid configuration here.
    # Return False if config is invalid.

    hcc2_logger.info("Provisioning Validation Successful")
    return True


# =============================================================================
#                              Main Application
# =============================================================================

def app():
    """Application setup and run."""

    info_banner(f"{AppConfig.app_name} ({AppConfig.app_version})")
    hcc2_logger.info(f"Supported REST Container Version {RestAPI.container_version}")
    hcc2_logger.info(f"Supported REST API Definition {RestAPI.api_version}")
    hcc2_logger.info(f"Waiting For REST Server...")


    #                         Wait For REST Server Up
    # =========================================================================
    hcc2_logger.info("Delaying 10 Seconds : Waiting For Rest Server")
    time.sleep(10)

    # Resolve IPs on Edgenet
    AppConfig.resolve_ips()
    hcc2_logger.info(f"REST Server IP: {AppConfig.rest_ip}")
    hcc2_logger.info(f"{AppConfig.app_name} IP: {AppConfig.app_ip}")
    rest_api = RestAPI()

    # Check Port 7071 is Open (REST API Port)
    if not rest_api.is_port_open():
        hcc2_logger.critical(f"Port 7071 is not open on {AppConfig.rest_ip}")
        sys.exit(ExitCode.REST_SERVER_PORT_NOT_OPEN)

    # Ping Rest Server
    if rest_api.ping(attempts=3):
        hcc2_logger.info("REST Server Found")
    else:
        hcc2_logger.critical("REST Server Could Not Be Found After 3 Attempts.")
        sys.exit(ExitCode.REST_SERVER_NOT_FOUND)


    #                             Registration
    # =========================================================================
    registration()

    # Delay (Core Application Registration Delay)
    hcc2_logger.info("Delaying 5 Seconds : Core Application Registration")
    time.sleep(5)


    #                              Heartbeat
    # =========================================================================
    heartbeat_thread = Heartbeat()
    heartbeat_thread.start()
    hcc2_logger.info("Starting Application Heartbeat")


    #                             Provisioning
    # =========================================================================
    provisioning_thread = Provisioning(validation_function=complex_provisioning_validation)
    provisioning_thread.start()
    hcc2_logger.info("Delaying 5 Seconds : First Provisioning")
    time.sleep(5)


    #                      Start Application Task Loop
    # =========================================================================
    info_banner(f"Starting Application {AppConfig.app_func_name}")

    if not Provisioning.is_provisioned:
        info_banner("Waiting On Provisioning Data")

    # Init task classes
    try:
        task1 = Task1()
        task1.start()

        task2 = Task2()
        task2.start()

    except Exception as exc:
        hcc2_logger.info(f"{AppConfig.app_func_name} failed due to exception: {exc}")
        hcc2_logger.info(f"Stopping {AppConfig.app_func_name}.")

        task1.stop()
        task2.stop()

        time.sleep(10) # Prevent rapid restarting on error
        sys.exit(ExitCode.UNEXPECTED_ERROR)
