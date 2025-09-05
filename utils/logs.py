"""logs.py

Logging utilites."""

import logging

# Local
from config import AppConfig

# Logging
hcc2_logger = logging.getLogger(AppConfig.app_func_name)
hcc2_logger.propagate = False


def info_banner(msg):
    """Log an info level banner."""

    hcc2_logger.info('---------------------------------------------')
    hcc2_logger.info(msg)
    hcc2_logger.info('---------------------------------------------')
