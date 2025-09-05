"""define_config_datapoints.py

Example: How to define and reference configuration data points within the DataPoints class.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from api.hcc2_rest_schema import (
    TagMetadata, TagUnityUI, ConfigDataPoint
)
from api.hcc2_rest_enums import (
    TagDataType, UnitType
)

# Import global data point dataclass
from utils import DataPoints


# Put these into the "Add Dynamic Config Data Points" section in app.py
# =============================================================================
#                         Add Dynamic Config Data Points
# =============================================================================

# Enable Voltage Out
DataPoints.add_config(
    ConfigDataPoint(
        topic="enabledVoltOut",
        defaultValue="true",

        # Bool
        metadata=TagMetadata(
            dataType=TagDataType.BOOL,
            unit=UnitType.NONE
        ),
        unityUI=TagUnityUI(
            displayName="Enable Voltage Out",
            shortDisplayName="enVoltOut",
            uiSize="3"
        )
    )
)

# Voltage Set
DataPoints.add_config(
    ConfigDataPoint(
        topic="voltageSet",
        defaultValue="24.0",

        # Float (Voltage)
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.VOLTAGE
        ),
        unityUI=TagUnityUI(
            displayName="Set Voltage",
            shortDisplayName="voltageSet",
            uiSize="3"
        )
    )
)

# Enable Current In
DataPoints.add_config(
    ConfigDataPoint(
        topic="enabledCurrIn",
        defaultValue="true",
        metadata=TagMetadata(
            dataType=TagDataType.BOOL,
            unit=UnitType.NONE
        ),
        unityUI=TagUnityUI(
            displayName="Enable Current In",
            shortDisplayName="enCurrIn",
            uiSize="3"
        )
    )
)

# Current Limit
DataPoints.add_config(
    ConfigDataPoint(
        topic="currentLimit",
        defaultValue="1.0",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.CURRENT
        ),
        unityUI=TagUnityUI(
            displayName="Current Limit",
            shortDisplayName="currLimit",
            uiSize="3"
        )
    )
)

# Cycle Period
DataPoints.add_config(
    ConfigDataPoint(
        topic="cyclePeriodSec",
        defaultValue="3",
        metadata=TagMetadata(
            dataType=TagDataType.UINT32,
            unit=UnitType.NONE
        ),
        unityUI=TagUnityUI(
            displayName="Cycle Period",
            shortDisplayName="cyclePeriodSec",
            uiSize="3"
        )
    )
)

# Duty Cycle
DataPoints.add_config(
    ConfigDataPoint(
        topic="dutyCycle",
        defaultValue="50.0",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.PERCENT,
            min="0",
            max="100"
        ),
        unityUI=TagUnityUI(
            displayName="Duty Cycle",
            shortDisplayName="dutyCycle",
            uiSize="3"
        )
    )
)

# Offset
DataPoints.add_config(
    ConfigDataPoint(
        topic="offset",
        defaultValue="-18",
        metadata=TagMetadata(
            dataType=TagDataType.INT16,
            unit=UnitType.NONE
        ),
        unityUI=TagUnityUI(
            displayName="Offset",
            shortDisplayName="offset",
            uiSize="3"
        )
    )
)

# SMS Notification Number
DataPoints.add_config(
    ConfigDataPoint(
        topic="smsNumber",
        defaultValue="+1 555-123-4567",
        metadata=TagMetadata(
            dataType=TagDataType.STRING,
            unit=UnitType.NONE
        ),
        unityUI=TagUnityUI(
            displayName="SMS Note Number",
            shortDisplayName="smsNumber",
            uiSize="3"
        )
    )
)

# JSON String App Settings
DataPoints.add_config(
    ConfigDataPoint(
        topic="appSettings",
        defaultValue='{"settings": [{"settingName": "PressureThreshold", "value": 3500}]}',
        metadata=TagMetadata(
            dataType=TagDataType.JSON,
            unit=UnitType.NONE
        ),
        unityUI=TagUnityUI(
            displayName="App Settings",
            shortDisplayName="appSettings",
            uiSize="12"
        )
    )
)

# Tag Selection
DataPoints.add_config(
    ConfigDataPoint(
        topic="tagSelect",
        defaultValue="None",
        metadata=TagMetadata(
            dataType=TagDataType.TAG,
            unit=UnitType.NONE
        ),
        unityUI=TagUnityUI(
            displayName="Tag Selection",
            shortDisplayName="tagSelect",
            uiSize="12"
        )
    )
)


# Added data points are referenced by their topic from the "config" simple namespace.

# Print out config data points
print("Added Config Datapoint FQNs")
print(DataPoints.config.enabledVoltOut)
print(DataPoints.config.voltageSet)
print(DataPoints.config.enabledCurrIn)
print(DataPoints.config.currentLimit)
print(DataPoints.config.cyclePeriodSec)
print(DataPoints.config.dutyCycle)
print(DataPoints.config.offset)
print(DataPoints.config.smsNumber)
print(DataPoints.config.appSettings)
print(DataPoints.config.tagSelect)

print("\n")

# Print config data point default values
print("Added Config Datapoint Default Values")
print(DataPoints.config.enabledVoltOut.defaultValue)
print(DataPoints.config.voltageSet.defaultValue)
print(DataPoints.config.enabledCurrIn.defaultValue)
print(DataPoints.config.currentLimit.defaultValue)
print(DataPoints.config.cyclePeriodSec.defaultValue)
print(DataPoints.config.dutyCycle.defaultValue)
print(DataPoints.config.offset.defaultValue)
print(DataPoints.config.smsNumber.defaultValue)
print(DataPoints.config.appSettings.defaultValue)
print(DataPoints.config.tagSelect.defaultValue)
