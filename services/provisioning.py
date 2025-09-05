"""provisioning.py

Thread class to manage incoming provisioning data for review.
"""

import sys
import time
import logging
import json
import tarfile
import threading
from http import HTTPStatus
from urllib.parse import urljoin

# Third party
import requests

# Local
from api import RestAPI
from config import AppConfig, ExitCode
from utils import info_banner

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


class PostValidConfig:
    """Post valid configuration values. 
    
    The provisioning thread will update these when an HCC2 deployment occurs.

    If complex provisioning is enable and the new config is rejected this class
    will not update.
    """
    _lock = threading.Lock()
    _dict = {}

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is class-level access only.")

    @classmethod
    def update(cls, topic : str, value) -> None:
        """Add a configuration datapoint."""
        with cls._lock:
            cls._dict[topic] = value

    @classmethod
    def value(cls, topic):
        """Return current provisioned value or configured default value."""
        with cls._lock:
            try:
                return cls._dict[topic]
            except KeyError:
                hcc2_logger.error(f"Provisioning config value {topic} not found!")

    @classmethod
    def list(cls) -> None:
        """Print a list of current configuration registers and values."""
        hcc2_logger.info("Current Post Valid Config:")
        [hcc2_logger.info(f" - {item} : {value}") for item, value in cls._dict.items()]


class Provisioning(threading.Thread):
    """Application provisioning thread.
    
    This thread polls for new provisioning data on the event of an HCC2 deployment.

    New provisioning TAR.GZ data is loaded into the PostValidConfig dataclass.
    """
    is_provisioned = False

    def __init__(self, validation_function):
        """Initialize the provisioning thread."""
        super().__init__()
        self.rest = RestAPI(version=1)
        self.validation_function = validation_function
        self.pre_valid_config = {}

    def _get_pre_valid_config_data(self) -> bool:
        """Get provisioning TAR.GZ from REST server.
        Store data into self.pre_valid_config dictionary."""

        targz_data = self.rest.get_targz_app(AppConfig.app_func_name)

        # Get parameters_this_0.json data from TAR.GZ
        try:
            with tarfile.open(fileobj=targz_data, mode="r:gz") as tar:
                member = tar.getmember('parameters_this_0.json')
                with tar.extractfile(member) as f:
                    if f:
                        self.pre_valid_config = json.load(f)
                    else:
                        raise IOError("Failed to extract parameters_this_0.json from the tarball")

        except ValueError:
            hcc2_logger.info('No config data found!')
            return False

        return True

    def _update_post_valid_config(self):
        """Get post valid config data from HCC2 message reads."""

        hcc2_logger.info('Reading All Post Valid Config Values.')

        for topic in self.pre_valid_config.keys():
            if topic != 'hash':
                try:
                    value = self.rest.message_read_simple(f"liveValue.postvalidConfig.this.{AppConfig.app_func_name}.0.{topic}.")[0].value

                except IndexError:
                    hcc2_logger.info(f'Configuration value {topic} could not be read from Live Data.')
                    value = None

                except Exception as exc:
                    hcc2_logger.info(f'Could not read configuration value {topic} due to exception {exc}')
                    value = None

                PostValidConfig.update(topic, value)

        Provisioning.is_provisioning = True

    def _validate(self):
        """Validate pre-valid configuration data using the provided validation function."""

        if AppConfig.provisioning_complex:

            # Use the provided validation function for complex provisioning only
            try:
                is_valid = self.validation_function(self)
            except Exception as exc:
                hcc2_logger.error(f"Complex provisioning function failed due to exception: {exc}")
                is_valid = False

        else:
            is_valid = True

        # POST Validation Result
        response = requests.post(
            urljoin(self.rest.url, f"app-provision/{AppConfig.app_func_name}"),
            json={"isValid": is_valid},
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        if (response.status_code == HTTPStatus.NO_CONTENT) or response.ok:
            hcc2_logger.info(f'Provisioning complete. Result {("Pass" if is_valid else "Fail")}')

        if (not is_valid) and AppConfig.provisioning_exit_if_failed:
            sys.exit(ExitCode.PROVISIONING_FAILED)

        return is_valid

    def run(self):
        while AppConfig.running():
            try:
                # Get provisioning status
                response = requests.get(
                    urljoin(self.rest.url, f'app-provision/{AppConfig.app_func_name}'),
                    timeout=5
                )

                # Continue if bad request
                if response.status_code != HTTPStatus.OK:
                    hcc2_logger.error(f'Failed to fetch new provisioning data: {response.text}')
                    time.sleep(AppConfig.provisioning_poll + 10)
                    continue

                # Continue if no provisioning data
                if not response.json().get('hasNewConfig'):
                    time.sleep(AppConfig.provisioning_poll)
                    continue

                info_banner(f'Provisioning : {('Complex' if AppConfig.provisioning_complex else 'Simple')}')

                # Save JSON provisioning data to memory
                if not self._get_pre_valid_config_data():
                    time.sleep(AppConfig.provisioning_poll)
                    continue

                # Validate provisioning data
                validation_result = self._validate()

                self._update_post_valid_config()
                time.sleep(AppConfig.provisioning_poll)

                # Set provisioning status
                Provisioning.is_provisioned = (
                    validation_result if AppConfig.provisioning_complex else True
                )

                PostValidConfig.list()

            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                hcc2_logger.error("Provisioning fetch failed.")
                time.sleep(10)

            except Exception as exc:
                hcc2_logger.error(f"A provisoning error occurred: {exc}")
                time.sleep(10)

    def stop(self):
        """Stop provisioning thread."""
        hcc2_logger.info(f'Stopping {AppConfig.app_func_name}')
