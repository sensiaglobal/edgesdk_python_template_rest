"""hcc2_rest_enums.py

Enumerations of common REST attributes.
These enumerations resolve only to their string values for all API calls.
"""


class TagCategory():
    """HCC2 tag category."""

    GENERAL = "general"
    CONFIG = "config"


class MessageQuality():
    """HCC2 message quality."""

    GOOD = 192
    BAD = 8
    GOOD_LOCAL_OVERRIDE = 216
    GOOD_LOCAL_OVERRIDE_CONSTANT = 219
    STALE = 64
    MINIMUM_OUT_OF_RANGE = 65
    MAXIMUM_OUT_OF_RANGE = 66
    FROZEN = 67
    INVALID_FACTOR_OFFSET = 68
    SET_ITEM_INACTIVE = 28
    COMMUNICATION_FAILURE = 24
    UNABLE_TO_PARSE = 4
    DEVICE_NOT_CONNECTED = 8


class TagSubClass():
    """General tag subclass."""

    PRODUCTION = "production"
    DIAGNOSTICS = "diagnostics"
    STATE = "state"


class TagDataType():
    """HCC2 application tag datatypes."""

    BOOL = "Bool"
    UINT8 = "Uint8"
    UINT16 = "Uint16"
    UINT32 = "Uint32"
    UINT64 = "Uint64"
    INT8 = "Int8"
    INT16 = "Int16"
    INT32 = "Int32"
    INT64 = "Int64"
    FLOAT = "Float"
    DOUBLE = "Double"
    STRING = "String"
    JSON = "JSON"
    ENUM = "Enum"
    TAG = "Tag"


class UnitType():
    """HCC2 application tag units."""

    NONE = "NONE"
    FACTOR = "FACT"
    FRACTION = "FRAC"
    PERCENT = "PRCNT"
    MICRO_VOLUME = "UGVOL"
    ULTRA_LOW_VOLUME = "ULVOL"
    GAS_VOLUME = "GVOL"
    LIQUID_VOLUME = "LVOL"
    SPECIFIC_AREA = "SPA"
    SPECIFIC_GRAVITY = "SPG"
    DIFFERENTIAL_PRESSURE = "DP"
    TEMPERATURE = "TEMP"
    MASS = "MASS"
    LENGTH = "LEN"
    FORCE = "FORCE"
    TORQUE = "TORQUE"
    ACCELERATION = "ACC"
    ANGLE = "ANGLE"
    ENERGY = "ENER"
    CURRENT = "CUR"
    VOLTAGE = "VOLT"
    POWER = "POW"
    APPARENT_POWER = "POWAPP"
    CHARGE = "CHRG"
    RESISTANCE = "RES"
    INDUCTANCE = "IND"
    CAPACITANCE = "CAP"
    POWER_LEVEL = "POWLEV"
    FREQUENCY = "FREQ"
    TIME = "TIME"
    RUNTIME = "RUNTIME"
    SYSTEM_PERIOD = "SYSPER"
    SYSTEM_TIME = "SYSTIME"
    VISCOSITY = "VISC"
    DENSITY_ABSOLUTE = "DENSA"
    DENSITY_RELATIVE = "DENSR"
    MASS_DENSITY = "MDENS"
    MOLAR_MASS = "MMASS"
    MASS_FRACTION = "MFRAC"
    MEGA_HIGH_VOLTAGE = "MHV"
    VERY_HIGH_VOLTAGE = "VHV"
    ENERGY_PER_MASS = "EPM"
    TIME_EXPONENT = "TEXP"
    PEAK_PRESSURE_GRADIENT = "PPGV"
    PEAK_POWER_LEVEL = "PPLV"
    PARTS_PER_MILLION = "PPM"
    BIT_SHIFT_WEIGHT = "BSW"
    BYTE = "BYTE"


class BuiltInEnum():
    """Built in HCC2 enumerations."""

    ALARMLEVEL = "AlarmLevel_t"
    ALARMPUBLISHREASON = "AlarmPublishReason_t"
    BAD_GOOD = "BAD_GOOD_t"
    CIPDATATYPE = "CIPDataType_t"
    CSDATATYPE = "CSDataType_t"
    DECIMATIONALGORITHM = "DecimationAlgorithm_t"
    DIS_EN = "DIS_EN_t"
    ENIPCLNTITEMDIR = "EnipClntItemDir_t"
    ENIPCLNTITEMORIGIN = "EnipClntItemOrigin_t"
    EVENTCONDITION = "EventCondition_t"
    EVENTPUBLISHREASON = "EventPublishReason_t"
    IOB_DATATYPE = "IOB_DataType_t"
    IOB_FUNCTIONIDENTIFIERS = "IOB_FunctionIdentifiers_t"
    ISA_DATATYPES = "Isa_DataTypes_t"
    ISAVARMODE = "ISaVarMode_t"
    LICENSESTATUS = "LicenseStatus_t"
    LOGGINGPRIORITY = "LoggingPriority_t"
    MODBUSEXCEPTION = "ModbusException_t"
    NO_YES = "NO_YES_t"
    NOTRUN_RUN = "NOTRUN_RUN_t"
    OFF_ON = "OFF_ON_t"
    PROTOBUFDATATYPE = "ProtobufDataType_t"
    SERIALBAUD = "SerialBaud_t"
    SERIALPARITY = "SerialParity_t"
    SERIALSTOPBITS = "SerialStopBits_t"
    TAGPUBBEHAVIOR = "TagPubBehavior_t"
    TAGQUALITY = "TagQuality_t"
    TAGSUBBEHAVIOR = "TagSubBehavior_t"
