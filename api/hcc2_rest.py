"""hcc2_rest.py

REST API utility class.
"""

import os
import io
import sys
import socket
import logging
from typing import Union, List
from urllib.parse import urljoin

# Third party
import requests
from requests import Response
from requests.exceptions import RequestException

# Local
from api.hcc2_rest_schema import (
    GeneralDataPoint, ConfigDataPoint, 
    SimpleMessage, ComplexMessage, DataPoint
)
from api.hcc2_rest_enums import (
    TagCategory
)
from config import AppConfig

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


class RestAPI:
    """A class to interact with the HCC2 REST Server."""

    container_version = "0.1.0-r20250219.3"
    api_version = "V1"

    def __init__(self, version=1):
        self.version = version
        self.timeout = 3

    @property
    def url(self):
        """Rest API base URL"""
        return f'http://{AppConfig.rest_ip}:{AppConfig.rest_port}/api/v{self.version}/'


    # Ping
    def ping(self, attempts=3) -> bool:
        """Ping for Rest Server life with a simple message read."""
        attempt = 0
        while attempt < attempts:
            try:
                response = self.check_provisioning_status(AppConfig.app_func_name)
                if response is not None:
                    return True
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                hcc2_logger.error(f"HCC2 Rest server ping attempt {attempt+1} failed!")
            attempt += 1
        return False

    def is_port_open(self):
        """Check if a port is open on a given IP."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:
                s.connect((AppConfig.rest_ip, AppConfig.rest_port))
                return True
            except Exception:
                return False


    # Data Points
    def create_datapoints(self, app_name: str, tag_type: Union[TagCategory, str], tag_list: List[Union[GeneralDataPoint, ConfigDataPoint, dict]]) -> Response:
        """Create a general or config data point for an application within the app-creator"""

        # Convert tag list to dict
        tag_json = {"tagsList": [topic.to_dict() if isinstance(topic, (GeneralDataPoint, ConfigDataPoint)) else topic for topic in tag_list]}

        return requests.request(
            "PUT",
            urljoin(self.url, f"app-creator/{app_name}/datapoint/{tag_type}"),
            json=tag_json,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )


    # Initialize Application
    def initialize_app(self, app_name: str) -> Response:
        """Create an empty application."""

        return requests.request(
            "PUT",
            urljoin(self.url, f"app-creator/{app_name}/defaults"),
            timeout=self.timeout
        )

    def open_app(self, app_name: str, config_file: str) -> requests.Response:
        """Open an application with an existing configuration TAR.GZ file."""

        # Validate file exists
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"The configuration file '{config_file}' was not found.")

        # POST within open file context
        with open(config_file, "rb") as file:
            files = {
                "appFile": (f"{AppConfig.app_func_name}.tar.gz", file, "application/octet-stream")
            }

            try:
                response = requests.post(
                    urljoin(self.url, f"app-creator/{app_name}"),
                    files=files,
                    timeout=self.timeout
                )
                response.raise_for_status()

                return response

            except requests.exceptions.RequestException as e:

                raise RuntimeError(f"Failed to open app '{app_name}': {e}")


    # Provisioning
    def heartbeat_app(self, app_name: str, is_up=True) -> Response:
        """Emit application heartbeat."""

        return requests.request(
            "PUT",
            urljoin(self.url, f"app-provision/{app_name}"),
            json={"isUp": is_up},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

    def check_provisioning_status(self, app_name: str) -> bool:
        """Check on the provisioning status of an application."""

        response = requests.request(
            "GET",
            urljoin(self.url, f"app-provision/{app_name}"),
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

        if response.ok:
            return response.json()["hasNewConfig"]

        return False

    def get_targz_app(self, app_name: str) -> io.BytesIO:
        """Fetch provisioning TAR.GZ data. Returns the data as a file object."""

        try:
            response = requests.get(
                urljoin(self.url, f"app-provision/{app_name}/targz"),
                timeout=self.timeout,
                stream=True)

            response.raise_for_status()

            tar_gz_memory = io.BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                tar_gz_memory.write(chunk)

            # Reset buffer
            tar_gz_memory.seek(0)

            return tar_gz_memory

        except RequestException:
            return None


    # Registration
    def register_app(self, app_name: str, config_file=None, is_complex_provisioned=False) -> Response:
        """Register an application with a configuration tar.gz file."""

        query_params = {
            "isComplexProvisioned": str(is_complex_provisioned).lower()
        }

        if config_file:
            with open(config_file, "rb") as file:
                files = {
                    "formFile": ("config_file", file, "application/octet-stream")
                }

        else:
            files = None

        return requests.request(
            "POST",
            urljoin(self.url, f"app-registration/{app_name}"),
            params=query_params,
            files=files,
            timeout=self.timeout
        )


    # Messages
    def message_read_simple(self, topics: List[Union[GeneralDataPoint, ConfigDataPoint, str]]) -> list[SimpleMessage]:
        """Read any number of simple tag topics. Returns as list of SimpleMessage."""

        if not isinstance(topics, list):
            topics = [topics]

        # Resolve data point dataclasses to their tag topic string (FQN)
        topics = [t.fqn if isinstance(t, (GeneralDataPoint, ConfigDataPoint)) else t for t in topics]

        response = requests.request(
            "POST",
            urljoin(self.url, "message/read"),
            json={"topics": topics, "includeOptional": True},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

        if response.ok:
            return [
                SimpleMessage(
                    j['topic'],
                    j['value'],
                    j['msgSource'],
                    j['quality'],
                    j['timeStamp']
                )
                for j in response.json()]

        return []

    def message_read_complex(self, topics: List[str]) -> list[ComplexMessage]:
        """Read any number of simple or complex tag topics. Returns as list of ComplexMessage."""

        if not isinstance(topics, list):
            topics = [topics]

        response = requests.request(
            "POST",
            urljoin(self.url, "message/read-advanced"),
            json={"topics": topics},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

        if response.ok:
            response_json = response.json()
            return [
                ComplexMessage(
                    j['topic'],
                    [DataPoint(
                        i['dataPointName'],
                        i['values'],
                        i['quality'],
                        i['timeStamps']
                        )
                        for i in j['datapoints']
                    ],
                    j['msgSource'],
                )
                for j in response_json]

        return []

    def message_write_simple(self, topics: List[Union[SimpleMessage, dict]]) -> Response:
        """Write any number of simple tag topcis."""

        if not isinstance(topics, list):
            topics = [topics]

        messages = [topic.to_dict() if isinstance(topic, SimpleMessage) else topic for topic in topics]

        return requests.request(
            "POST",
            urljoin(self.url, "message/write"),
            json=messages,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

    def message_write_complex(self, topics: List[Union[SimpleMessage, ComplexMessage, dict]]) -> Response:
        """Write any number of simple or complex tag topcis."""

        if not isinstance(topics, list):
            topics = [topics]

        messages = [topic.to_dict() if isinstance(topic, (SimpleMessage, ComplexMessage)) else topic for topic in topics]

        return requests.request(
            "POST",
            urljoin(self.url, "message/write-advanced"),
            json=messages,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

    def message_list(self, topic_filter : str) -> dict:
        """Return a list of filter tag topics."""

        response = requests.request(
            "POST",
            urljoin(self.url, "message/list"),
            json={"topics": [topic_filter]},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

        if response.ok:
            return response.json()

        return None


    # Subscriptions
    def subscribe(self, app_name: str, callback: str, topic: str) -> str:
        """Subscibe to a HCC2 message."""

        json_data = {
            "callbackAPi": callback, 
            "topics": [topic],
            "includeOptional": True}

        response = requests.request(
            "POST",
            urljoin(self.url, f"message/subscription/{app_name}"),
            json=json_data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )

        if response.ok:
            return callback

        return ""

    def unsubscribe(self, app_name: str, topic: str) -> Response:
        """Unsubscribe from a HCC2 message."""

        return requests.request(
            "DELETE",
            urljoin(self.url, f"message/subscription/{app_name}/{topic}"),
            timeout=self.timeout
        )
