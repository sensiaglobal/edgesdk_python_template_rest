"""define_general_datapoints.py

Example: How to define and reference general data points within the DataPoints class.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Local
from api.hcc2_rest_schema import (
    TagMetadata, TagUnityUI, GeneralDataPoint
)
from api.hcc2_rest_enums import (
    TagDataType, TagSubClass, UnitType
)

# Import global data point dataclass
from utils import DataPoints


# Put these into the "Add Dynamic General Data Points" section in app.py
# =============================================================================
#                         Add Dynamic General Data Points
# =============================================================================

# Bool Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="inputs.boolIn",
        metadata=TagMetadata(
            dataType=TagDataType.BOOL,
            unit=UnitType.NONE,
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="Bool Input",
            shortDisplayName="boolIn",
            uiSize="1"
        )
    )
)

# Int32 Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="inputs.int32In",
        metadata=TagMetadata(
            dataType=TagDataType.INT32,
            unit=UnitType.NONE,
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="Int32 Input",
            shortDisplayName="int32In",
            uiSize="3"
        )
    )
)

# String Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="inputs.stringIn",
        metadata=TagMetadata(
            dataType=TagDataType.STRING,
            unit=UnitType.NONE,
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="String Input",
            shortDisplayName="stringIn",
            uiSize="3"
        )
    )
)

# JSON String Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="inputs.jsonIn",
        metadata=TagMetadata(
            dataType=TagDataType.JSON,
            unit=UnitType.NONE,
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="Json Input",
            shortDisplayName="jsonIn",
            uiSize="3"
        )
    )
)

# Voltage Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.STATE,
        topic="inputs.voltageIn",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.VOLTAGE,
            min="-30",
            max="30",
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="Voltage (V) Input",
            shortDisplayName="voltageIn",
            uiSize="3"
        )
    )
)

# Current Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.STATE,
        topic="inputs.currentIn",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.CURRENT,
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="Current (A) Input",
            shortDisplayName="currentIn",
            uiSize="3"
        )
    )
)

# Percent Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.STATE,
        topic="inputs.percentIn",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.PERCENT,
            min="0",
            max="100",
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="Percent Input",
            shortDisplayName="percentIn",
            uiSize="3"
        )
    )
)

# Temperature Input
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.STATE,
        topic="inputs.tempIn",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.TEMPERATURE,
            min="-273.15",
            isInput="true",
            isOutput="false"
        ),
        unityUI=TagUnityUI(
            displayName="Temperature Input",
            shortDisplayName="tempIn",
            uiSize="3"
        )
    )
)

# Bool Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="outputs.boolOut",
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
        topic="outputs.int32Out",
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

# Voltage Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.PRODUCTION,
        topic="outputs.voltageOut",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.VOLTAGE,
            min="-30",
            max="30",
            isInput="false",
            isOutput="true"
        ),
        unityUI=TagUnityUI(
            displayName="Voltage (V) Output",
            shortDisplayName="voltageOut",
            uiSize="3"
        )
    )
)

# Current Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.DIAGNOSTICS,
        topic="outputs.currentOut",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.CURRENT,
            isInput="false",
            isOutput="true"
        ),
        unityUI=TagUnityUI(
            displayName="Current (A) Output",
            shortDisplayName="currentOut",
            uiSize="3"
        )
    )
)

# Percent Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.DIAGNOSTICS,
        topic="outputs.percentOut",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.PERCENT,
            min="0",
            max="100",
            isInput="false",
            isOutput="true"
        ),
        unityUI=TagUnityUI(
            displayName="Percent Output",
            shortDisplayName="percentOut",
            uiSize="3"
        )
    )
)

# Temperature Output
DataPoints.add_general(
    GeneralDataPoint(
        tagSubClass=TagSubClass.DIAGNOSTICS,
        topic="outputs.tempOut",
        metadata=TagMetadata(
            dataType=TagDataType.FLOAT,
            unit=UnitType.TEMPERATURE,
            min="-273.15",
            isInput="false",
            isOutput="true"
        ),
        unityUI=TagUnityUI(
            displayName="Temperature Output",
            shortDisplayName="tempOut",
            uiSize="3"
        )
    )
)


# Added data points are referenced by their topic from the "config" simple namespace.

# Print out config data points
print("Added General Datapoint FQNs")
print(DataPoints.general.inputs_boolIn)
print(DataPoints.general.inputs_int32In)
print(DataPoints.general.inputs_stringIn)
print(DataPoints.general.inputs_jsonIn)
print(DataPoints.general.inputs_voltageIn)
print(DataPoints.general.inputs_currentIn)
print(DataPoints.general.inputs_percentIn)
print(DataPoints.general.inputs_tempIn)
print(DataPoints.general.outputs_boolOut)
print(DataPoints.general.outputs_int32Out)
print(DataPoints.general.outputs_voltageOut)
print(DataPoints.general.outputs_currentOut)
print(DataPoints.general.outputs_percentOut)
print(DataPoints.general.outputs_tempOut)

print("\n")

print("Added General Datapoint Subclasses")
print(DataPoints.general.inputs_boolIn.tagSubClass)
print(DataPoints.general.inputs_int32In.tagSubClass)
print(DataPoints.general.inputs_stringIn.tagSubClass)
print(DataPoints.general.inputs_jsonIn.tagSubClass)
print(DataPoints.general.inputs_voltageIn.tagSubClass)
print(DataPoints.general.inputs_currentIn.tagSubClass)
print(DataPoints.general.inputs_percentIn.tagSubClass)
print(DataPoints.general.inputs_tempIn.tagSubClass)
print(DataPoints.general.outputs_boolOut.tagSubClass)
print(DataPoints.general.outputs_int32Out.tagSubClass)
print(DataPoints.general.outputs_voltageOut.tagSubClass)
print(DataPoints.general.outputs_currentOut.tagSubClass)
print(DataPoints.general.outputs_percentOut.tagSubClass)
print(DataPoints.general.outputs_tempOut.tagSubClass)
