"""datapoints.py

Application data points global data class.
"""

from types import SimpleNamespace

# Local
from api.hcc2_rest_schema import (
    GeneralDataPoint, ConfigDataPoint
)


class DataPoints:
    """App data points data class."""

    general_points = []
    config_points = []

    # SimpleNamespace variables to hold datapoints keyed by topic.
    general = SimpleNamespace()
    config = SimpleNamespace()

    @classmethod
    def add_general(cls, datapoint : GeneralDataPoint):
        """Add general datapoint to global data class."""

        # Create the namespace key.
        if datapoint.topic.startswith("liveValue."):
            key = ("".join(datapoint.topic.replace('.', "_.").split(".")[5:]).replace('.', '_'))[:-1]
        else:
            key = datapoint.topic.replace('.', '_')

        # Check if key already exists (Duplicated topics)
        if hasattr(cls.general, key):
            raise ValueError(f"General datapoint with Topic '{key}' already exists.")

        # Add data point
        cls.general_points.append(datapoint)
        setattr(cls.general, key, datapoint)

    @classmethod
    def add_config(cls, datapoint : ConfigDataPoint):
        """Add config datapoint to global data class."""

        # Create the namespace key.
        key = datapoint.topic.replace('.', '_')[:-1]

        # Check if key already exists (Duplicated topics)
        if hasattr(cls.config, key):
            raise ValueError(f"Config datapoint with Topic '{key}' already exists.")

        # Add data point
        cls.config_points.append(datapoint)
        setattr(cls.config, key, datapoint)
