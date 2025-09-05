"""setup_subscriptions.py

Example: Setup subscriptions to HCC2 tag topics.
"""

import os
import sys
import time

# Allows local imports in non-package script.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from api import RestAPI
from config import AppConfig
from services import Subscriptions


def setup_subscription():

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

    # Subscribe to HCC2 IO Board Rail Voltages
    Subscriptions.subscribe("liveValue.diagnostics.this.io.0.rail.voltage.v1p2.")
    Subscriptions.subscribe("liveValue.diagnostics.this.io.0.rail.voltage.v3p3.")
    Subscriptions.subscribe("liveValue.diagnostics.this.io.0.rail.voltage.v5.")

    # Delay 5 seconds for new data to come in.
    time.sleep(5)

    # Print latest rail voltag readings every 5 seconds
    while True:
        rail_voltage_1v2 = Subscriptions.active["liveValue.diagnostics.this.io.0.rail.voltage.v1p2."].latest()
        rail_voltage_3v3 = Subscriptions.active["liveValue.diagnostics.this.io.0.rail.voltage.v3p3."].latest()
        rail_voltage_5v0 = Subscriptions.active["liveValue.diagnostics.this.io.0.rail.voltage.v5."].latest()

        # io_temp_msg will be a SimpleMessage if data was published since last latest() call
        if rail_voltage_1v2 is not None:
            print(f"IO Board 1.2V Rail: {rail_voltage_1v2.value} V")

        if rail_voltage_3v3 is not None:
            print(f"IO Board 3.3V Rail: {rail_voltage_3v3.value} V")

        if rail_voltage_5v0 is not None:
            print(f"IO Board 5.0V Rail: {rail_voltage_5v0.value} V")

        print('\n')
        time.sleep(5)

setup_subscription()
