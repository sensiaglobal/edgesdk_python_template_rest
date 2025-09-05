"""send_read_complex_message.py

Example: Send a complex read request to the HCC2 rest server.
"""

import os
import sys

# Allows local imports in non-package script.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from api import RestAPI
from config import AppConfig


def example_send_read_complex_message():

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

    # Send read complex request (List of fully qualified tag topics)
    messages = rest_api.message_read_complex([

        # CPU Board Temperatures
        "liveValue.diagnostics.this.core.0.temperature|.",

        # CPU Board Usages
        "liveValue.diagnostics.this.core.0.cpuUsage|."
    ])

    # Print resonse values
    print(f"CPU Board Core Overall   : {messages[0].datapoints[0].values[0]} C")
    print(f"CPU Board Core 0 Temp    : {messages[0].datapoints[1].values[0]} C")
    print(f"CPU Board Core 1 Temp    : {messages[0].datapoints[2].values[0]} C")
    print(f"CPU Board Core 2 Temp    : {messages[0].datapoints[3].values[0]} C")
    print(f"CPU Board Core 3 Temp    : {messages[0].datapoints[4].values[0]} C")

    print(f"CPU Board Core Total     : {messages[1].datapoints[0].values[0]} %")
    print(f"CPU Board Core 0 Usage   : {messages[1].datapoints[1].values[0]} %")
    print(f"CPU Board Core 1 Usage   : {messages[1].datapoints[2].values[0]} %")
    print(f"CPU Board Core 2 Usage   : {messages[1].datapoints[3].values[0]} %")
    print(f"CPU Board Core 3 Usage   : {messages[1].datapoints[4].values[0]} %")

example_send_read_complex_message()
