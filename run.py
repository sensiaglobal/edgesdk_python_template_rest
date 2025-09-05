"""run.py

Application entry.
"""

import sys
import logging
from datetime import datetime, timezone

# Local
from app import app
from config import AppConfig, ExitCode

class HCC2Log(logging.Formatter):
    """HCC2 log formatter."""
    _version = 0

    def formatTime(self, record, datefmt=None):
        now = datetime.now(timezone.utc)
        return now.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

log_level = getattr(logging, AppConfig.app_log_level.upper(), logging.DEBUG)
logger = logging.getLogger(AppConfig.app_func_name)
logger.setLevel(log_level)

# DEBUG handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Format as HCC2 complient log messages
formatter = HCC2Log('[0][%(asctime)s][%(name)s][%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


if __name__ == '__main__':
    try:
        app()

    except SystemExit as e:
        hcc2_logger.info(f"Exit code: {e.code}")
        sys.exit(e.code)
    except Exception as e:
        hcc2_logger.info(f"Unexpected error: {e}")
        sys.exit(ExitCode.UNEXPECTED_ERROR)
