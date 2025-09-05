"""send_write_message.py

Example: Send a simple write request to the HCC2 rest server.
"""

import os
import sys

# Allows local imports in non-package script.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from api import RestAPI, SimpleMessage
from api.hcc2_rest_schema import (
    TagMetadata, TagUnityUI, GeneralDataPoint
)
from api.hcc2_rest_enums import (
    TagDataType, TagSubClass, UnitType
)

# Import global data point dataclass
from config import AppConfig
from utils import DataPoints


# Define some output general datapoints

# Bool Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="outputsBoolOut",
        metadata=TagMetadata(
            dataType=TagDataType.BOOL,
            unit=UnitType.NONE,
            isInput="false",
            isOutput="true"
        ),
        unityUI=TagUnityUI(
            displayName="Bool Output",
            shortDisplayName="boolOut",
            uiSize="1"
        )
    )
)

# Int32 Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="outputInt32",
        metadata=TagMetadata(
            dataType=TagDataType.INT32,
            unit=UnitType.NONE,
            isInput="false",
            isOutput="true"
        ),
        unityUI=TagUnityUI(
            displayName="Int32 Output",
            shortDisplayName="int32Out",
            uiSize="3"
        )
    )
)

# String Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="outputString",
        metadata=TagMetadata(
            dataType=TagDataType.STRING,
            unit=UnitType.NONE,
            isInput="false",
            isOutput="true"
        ),
        unityUI=TagUnityUI(
            displayName="String Output",
            shortDisplayName="stringOut",
            uiSize="3"
        )
    )
)


def example_send_write_message():

    # Resolve rest server IP address
    AppConfig.resolve_ips()

    # Init rest API utility class
    rest_api = RestAPI()

    # Check rest server is reachable
    if not rest_api.ping():
        print(f"Rest server {AppConfig.rest_ip} is not reachable!")
        return -1

    # Check port 7071 is open (REST API Port)
    if not rest_api.is_port_open():
        print(f"Port 7071 is not open on {AppConfig.rest_ip}!")
        return -1

    # Type the tag topic out manually.
    simple_msg_1 = SimpleMessage("liveValue.production.this.samplePythonApplication.0.outputsBoolOut.", 1)

    # Or reference the GeneralDataPoint class FQN
    simple_msg_2 = SimpleMessage(DataPoints.general.outputInt32.fqn, 30000)
    simple_msg_3 = SimpleMessage(DataPoints.general.outputString.fqn, "String Value")

    # Send write request (List of SimpleMessages)
    response = rest_api.message_write_simple([

        # Add Simple Messages
        simple_msg_1,
        simple_msg_2,
        simple_msg_3,
    ])

    # Check response
    if response.ok:
        print("All message written!")

    elif response.status_code == 404:
        print("This example cannot be run standalone. The tags defined above must be registered with the HCC2 before they can be written/read.")
        print(response.text)

example_send_write_message()
