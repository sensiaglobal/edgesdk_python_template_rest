"""hcc2_rest_schema.py

Dataclasses of REST schemas.
"""

import json
from datetime import datetime
from typing import Union, List, Any, Type, TypeVar
from dataclasses import dataclass, asdict, field

# Local
from config import AppConfig
from api.hcc2_rest_enums import (
    UnitType, TagDataType, TagSubClass, MessageQuality
)


# Ignore camel case dataclass fields naming complaints.
# pylint: disable=C0103

T = TypeVar('T', bound='Schema')
class Schema:
    """API schema utility function base dataclass."""

    def to_dict(self) -> dict:
        """Return dataclass as dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """Create an instance of the schema from a dictionary."""
        return cls(**data)

    def to_json(self) -> str:
        """Convert the schema to a JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Create an instance of the schema from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def update(self, **kwargs):
        """Update schema data with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def name(self) -> str:
        """Return the name of the schema."""
        return self.__class__.__name__


@dataclass
class TagMetadata(Schema):
    """
    Represents metadata for a config or general data point.

    Attributes:
    -----------
    dataType: str
        Data type of the tag (e.g., "float", "int").
    unit: str
        Unit of measurement (default: "NONE").
    min: Optional[str]
        Minimum allowed value (default: "0").
    max: Optional[str]
        Maximum allowed value (default: "0").
    noProtobuf: str
        Flag to exclude the tag from Protobuf serialization (default: "false").
    builtinEnums: Optional[str]
        Associated enumeration, if any (default: None).
    isInput: str
        Indicates if the tag is an input (default: "False").
    isOutput: str
        Indicates if the tag is an output (default: "True").
    arraySize: str
        Size of the tag array (default: "1").
    """
    dataType: Union[str, TagDataType]
    unit: str = UnitType.NONE
    min: str = "0"
    max: str = "0"
    noProtobuf: str = "false"
    builtinEnums: str = ""
    isInput: str = "true"
    isOutput: str = "false"
    arraySize: str = "1"


@dataclass
class TagUnityUI(Schema):
    """
    Represents Unity UI configuration for an application tag.

    Attributes:
    -----------
    displayName: str
        Full name displayed in the UI.
    shortDisplayName: str
        Abbreviated name for compact displays.
    configGroup: str
        Group Box to which this tag belongs in the HCC2 Unity UI.
    configSection: str
        Section within the group for this tag.
    displayMin: str
        Minimum display value for the tag.
    displayMax: str
        Maximum display value for the tag.
    uiSize: str
        Size of the widget in the HCC2 Unity UI.
    """
    displayName: str
    shortDisplayName: str
    configGroup: str = "Rest Tags"
    configSection: str = "Rest Tags"
    displayMin: str = "0"
    displayMax: str = "0"
    uiSize: str = "3"

    def __post_init__(self):
        if len(self.shortDisplayName) > 16:
            raise ValueError("shortDisplayName must be 16 characters or fewer")


@dataclass
class GeneralDataPoint(Schema):
    """
    General data point class.

    Attributes:
    -----------
    topic: str
        Tag topic name.
    tagSubClass: str
        Tag subclass, either production, diagnostic or status
    metadata: TagMetadata
        Metadata associated with the tag.
    unityUI: TagUnityUI
        Unity UI configuration for the tag.
    """
    topic: str
    tagSubClass: Union[str, TagSubClass]
    metadata: TagMetadata
    unityUI: TagUnityUI

    # Meaningless for General DPs but required by REST
    defaultValue: str = "0"

    def __post_init__(self):
        self.is_multitag = self.topic.endswith("|.")
        self.prefix = f'liveValue.{self.tagSubClass}.this.{AppConfig.app_func_name}.0.'
        self.fqn = self.topic if self.topic.startswith(self.prefix) else f'{self.prefix}{self.topic}'
        if not self.fqn.endswith('.'):
            self.fqn = self.fqn + '.'

        self.defaultValue = '0'
        self.value = None

    def __str__(self):
        return self.fqn


@dataclass
class ConfigDataPoint(Schema):
    """
    Configuration data point class.

    Attributes:
    -----------
    topic: str
        Tag topic name.
    metadata: TagMetadata
        Metadata associated with the tag.
    unityUI: TagUnityUI
        Unity UI configuration for the tag.
    defaultValue: str
        Default value for the tag.
    """
    topic: str
    metadata: TagMetadata
    unityUI: TagUnityUI
    defaultValue: str

    # Meaningless for Config DPs but required by REST
    tagSubClass: str = TagSubClass.PRODUCTION

    def __post_init__(self):
        self.is_multitag = self.topic.endswith("|.")
        self.prefix = f'liveValue.postvalidConfig.this.{AppConfig.app_func_name}.0.'
        self.fqn = self.topic if self.topic.startswith(self.prefix) else f'{self.prefix}{self.topic}'
        if not self.fqn.endswith('.'):
            self.fqn = self.fqn + '.'

        self.tagSubClass = TagSubClass.PRODUCTION
        self.value = None

    def __str__(self):
        return self.fqn


@dataclass
class SimpleMessage(Schema):
    """
    Represents a single tag message with associated value and metadata.

    Attributes:
    -----------
    topic: str
        Tag topic name.
    value: Any
        Value of the tag.
    msgSource: str
        Source application of the message.
    quality: int
        Quality of the message.
    timeStamp: int
        Timestamp of the message in milliseconds.
    """
    topic: str
    value: Any
    msgSource: str = AppConfig.app_func_name
    quality: int = MessageQuality.GOOD
    timeStamp: str = str(int(datetime.now().timestamp() * 1000))


@dataclass
class DataPoint(Schema):
    """
    Represents a sub-tag topic within a multi-tag message.

    Attributes:
    -----------
    dataPointName: str
        Name of the sub-tag topic.
    values: List[Any]
        List of values for the sub-tag topic.
    quality: int
        Quality of the data point message.
    timeStamps: List[int]
        List of timestamps corresponding to the values.
    """
    dataPointName: str
    values: List[Any] = field(default_factory=list)
    quality: int = MessageQuality.GOOD
    timeStamps: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.timeStamps = self.timeStamps if isinstance(self.timeStamps, list) else [self.timeStamps]
        self.values = self.values if isinstance(self.values, list) else [self.values]

        if self.quality == MessageQuality.GOOD:

            # Create list of current timestamp
            if not self.timeStamps:
                self.timeStamps = [str(int(datetime.now().timestamp() * 1000))] * len(self.values)


@dataclass
class ComplexMessage(Schema):
    """
    Represents a multi-tag message containing an array of DataPoints.

    Attributes:
    -----------
    topic: str
        Multi-tag topic name.
    datapoints: List[DataPoint]
        List of DataPoints within the multi-tag message.
    msgSource: str
        Source application of the message.
    """
    topic: str
    datapoints: List[DataPoint]
    msgSource: str = AppConfig.app_func_name
