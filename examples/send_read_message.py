"""send_read_message.py

Example: Send a simple read request to the HCC2 rest server.
"""

import os
import sys

# Allows local imports in non-package script.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from api import RestAPI
from config import AppConfig


def example_send_read_message():

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
        print(f"Port 7071 is not open on {AppConfig.rest_ip}")
        return -1

    # Send read request (List of fully qualified tag topics)
    messages = rest_api.message_read_simple([

        # IO Board Supply
        "liveValue.diagnostics.this.io.0.supplyPower.power.",
        "liveValue.diagnostics.this.io.0.supplyPower.current.",
        "liveValue.diagnostics.this.io.0.supplyPower.voltage."
    ])

    # Print resonse values
    print(f"IO Board Voltage     : {messages[0].value} V")
    print(f"IO Board Current     : {messages[1].value} A")
    print(f"IO Board Power Usage : {messages[2].value} W")

example_send_read_message()
