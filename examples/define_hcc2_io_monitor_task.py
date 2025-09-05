"""define_hcc2_io_monitor_task.py

Example: Define a new thread task to monitor the HCC2 DI1 and AI1 current values.

This is example code to be added under the Thread Task Defintions along side main and heartbeart tasks.
"""

import os
import sys
import time
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from app import Task
from config import AppConfig
from services import Subscriptions

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


# =============================================================================
#                           Threaded Task Defintions
# =============================================================================

class MonitorIOChannels(Task):
    """Subscribe and monitor HCC2 IO channels.
    
    DI1 : Monitor input state.
    - Log rising edge events.

    AI1 : Monitor engineering unit inst reading.
    - Log changes in max reading.
    """

    def __init__(self):
        super().__init__("Monitor IO Task")
        self._cycle_period = 1

        # Subscribe to HCC2 Digital Input 1 (Input State)
        Subscriptions.subscribe("liveValue.diagnostics.this.io.0.digitalIn.ch1.")
        self._last_dio_state = False

        # Subscribe to HCC2 Analog Input 1 (Inst EU Reading)
        Subscriptions.subscribe("liveValue.diagnostics.this.io.0.analogIn.eu.ch1.")
        self._ai_max = 0

    def execute(self):
        """Monitor IO Channel Values."""

        # Digital Input 1
        # Get SimpleMessage if DI1 has new subscription data, else None
        di1_state_message = Subscriptions.active["liveValue.diagnostics.this.io.0.digitalIn.ch1."].get()

        if di1_state_message is not None:
            di1_state = di1_state_message.value

            # Check for rising edge
            if (not self._last_dio_state) and di1_state:
                hcc2_logger.info("DI1 Rising Edge Detected.")

            self._last_dio_state = di1_state

        # Analog Input 1
        # Get latest AI1 value
        ai1_value_message = Subscriptions.active["liveValue.diagnostics.this.io.0.analogIn.eu.ch1."].latest()

        # Check for new AI1 EU max reading
        if ai1_value_message is not None:
            ai1_value = float(ai1_value_message.value)

            if ai1_value > self._ai_max:
                self._ai_max = ai1_value
                hcc2_logger.info(f"New AI1 EU Max Reading : {ai1_value}")

        # Delay the polling period
        time.sleep(self._cycle_period)


# Remember to add the task to the end of app() in app.py

# Init task classes
#    try:
#        heartbeat = HeartBeat()
#        heartbeat.start()
#
#        main = Main()
#        main.start()
#
#        io_monitor = MonitorIOChannels()
#        io_monitor.start()
#
#    except Exception as exc:
#        hcc2_logger.info(f"{AppConfig.app_func_name} failed due to exception: {exc}")
#        hcc2_logger.info(f"Stopping {AppConfig.app_func_name}.")
#
#        heartbeat.stop()
#        main.stop()
#        io_monitor.stop()
#
#        time.sleep(10) # Prevent rapid restarting on error
#        sys.exit(ExitCode.UNEXPECTED_ERROR)
