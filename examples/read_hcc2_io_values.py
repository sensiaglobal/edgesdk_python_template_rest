"""read_hcc2_io_values.py

Example: How to read HCC2 IO channel values.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from api import RestAPI
from config import AppConfig


def read_hcc2_io_values():
    """Read HCC2 IO Channel values."""

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

    # Digital Inputs
    di_input_states = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.digitalIn.ch1.",
        "liveValue.diagnostics.this.io.0.digitalIn.ch2.",
        "liveValue.diagnostics.this.io.0.digitalIn.ch3.",
        "liveValue.diagnostics.this.io.0.digitalIn.ch4.",
        "liveValue.diagnostics.this.io.0.digitalIn.ch5.",
        "liveValue.diagnostics.this.io.0.digitalIn.ch6.",
        "liveValue.diagnostics.this.io.0.digitalIn.ch7.",
        "liveValue.diagnostics.this.io.0.digitalIn.ch8."
    ])
    print("Digital Input States")
    print([msg.value for msg in di_input_states], "\n")

    di_input_counter_values = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.digitalInCount.ch1.",
        "liveValue.diagnostics.this.io.0.digitalInCount.ch2.",
        "liveValue.diagnostics.this.io.0.digitalInCount.ch3.",
        "liveValue.diagnostics.this.io.0.digitalInCount.ch4.",
        "liveValue.diagnostics.this.io.0.digitalInCount.ch5.",
        "liveValue.diagnostics.this.io.0.digitalInCount.ch6.",
        "liveValue.diagnostics.this.io.0.digitalInCount.ch7.",
        "liveValue.diagnostics.this.io.0.digitalInCount.ch8."
    ])
    print("Digital Inputs Counter Values")
    print([msg.value for msg in di_input_counter_values], "\n")

    # Digital Inputs/Outputs (Input Mode)
    dio_input_states = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch1.",
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch2.",
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch3.",
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch4.",
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch5.",
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch6.",
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch7.",
        "liveValue.diagnostics.this.io.0.digitalIoIn.ch8."
    ])
    print("Digital Inputs/Output Input States")
    print([msg.value for msg in dio_input_states], "\n")

    dio_input_counter_values = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch1.",
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch2.",
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch3.",
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch4.",
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch5.",
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch6.",
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch7.",
        "liveValue.diagnostics.this.io.0.digitalIoCount.ch8."
    ])
    print("Digital Inputs/Output Input Counter Values")
    print([msg.value for msg in dio_input_counter_values], "\n")

    # Digital Inputs/Outputs (Output Mode)
    dio_output_states = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch1.",
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch2.",
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch3.",
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch4.",
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch5.",
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch6.",
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch7.",
        "liveValue.diagnostics.this.io.0.digitalIoOut.ch8.",
    ])
    print("Digital Inputs/Outputs Output States")
    print([msg.value for msg in dio_output_states], "\n")

    # Digital Inputs/Outputs (PWM Output Mode)
    dio_output_pwm_dutycycle = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch1.",
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch2.",
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch3.",
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch4.",
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch5.",
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch6.",
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch7.",
        "liveValue.diagnostics.this.io.0.digitalIoDuty.ch8."
    ])
    print("Digital Inputs/Outputs Duty Cycles")
    print([msg.value for msg in dio_output_pwm_dutycycle], "\n")

    # Analog Inputs
    ai_eu_values = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch1.",
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch2.",
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch3.",
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch4.",
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch5.",
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch6.",
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch7.",
        "liveValue.diagnostics.this.io.0.analogIn.eu.ch8."
    ])
    print("Analog Inputs EU Values")
    print([msg.value for msg in ai_eu_values], "\n")

    ai_percent_values = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch1.",
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch2.",
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch3.",
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch4.",
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch5.",
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch6.",
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch7.",
        "liveValue.diagnostics.this.io.0.analogIn.perc.ch8.",
    ])
    print("Analog Inputs Percent Values")
    print([msg.value for msg in ai_percent_values], "\n")

    # Analog Outputs
    ao_percent_values = rest_api.message_read_simple([
        "liveValue.diagnostics.this.io.0.analogOut.ch1.",
        "liveValue.diagnostics.this.io.0.analogOut.ch2.",
    ])
    print("Analog Outputs Percent Values")
    print([msg.value for msg in ao_percent_values], "\n")


read_hcc2_io_values()
