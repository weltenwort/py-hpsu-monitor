from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Literal, Optional, TypeVar, Union

from paho.mqtt.client import MQTTMessage
from pydantic import BaseModel
from pydantic.tools import parse_raw_as

from .elster_frame import ElsterReadResponseFrame, ElsterWriteFrame

ValueType = TypeVar("ValueType")
RegisterDefinitionType_co = TypeVar("RegisterDefinitionType_co", covariant=True)


@dataclass(frozen=True)
class RegisterValue(Generic[ValueType, RegisterDefinitionType_co]):
    register_type: RegisterDefinitionType_co
    timestamp: float
    value: ValueType


class BaseRegisterDefinition(BaseModel, ABC):
    kind: str = "register"
    elster_index: int
    name: str
    owner_id: int

    class Config:
        allow_mutation = False


class ReadableRegisterDefinition(BaseRegisterDefinition):
    @abstractmethod
    def parse_elster_frame(
        self, frame: ElsterReadResponseFrame
    ) -> RegisterValue[Any, "ReadableRegisterDefinition"]:
        raise NotImplementedError()


class WritableRegisterDefinition(BaseRegisterDefinition):
    @abstractmethod
    def parse_mqtt_write_message(self, message: MQTTMessage) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def create_elster_write_frame(
        self,
        sender_id: int,
        value: RegisterValue[Any, "WritableRegisterDefinition"],
    ) -> ElsterWriteFrame:
        raise NotImplementedError()


class NumberSensorRegisterDefinition(ReadableRegisterDefinition):
    kind: Literal["number-sensor"] = "number-sensor"
    factor: float = 1.0
    unit: Optional[str] = None

    def parse_elster_frame(self, frame: ElsterReadResponseFrame):
        return RegisterValue(
            register_type=self,
            timestamp=frame.timestamp,
            value=frame.value * self.factor,
        )


class NumberSettingRegisterDefinition(
    ReadableRegisterDefinition, WritableRegisterDefinition
):
    kind: Literal["number-setting"] = "number-setting"
    factor: float = 1.0

    def parse_elster_frame(self, frame: ElsterReadResponseFrame):
        return RegisterValue(
            register_type=self,
            timestamp=frame.timestamp,
            value=frame.value * self.factor,
        )

    def parse_mqtt_write_message(self, message: MQTTMessage):
        return RegisterValue(
            register_type=self,
            timestamp=message.timestamp,
            value=parse_raw_as(float, message.payload),
        )

    def create_elster_write_frame(
        self,
        sender_id: int,
        value: RegisterValue[float, WritableRegisterDefinition],
    ):
        return ElsterWriteFrame(
            timestamp=value.timestamp,
            sender=sender_id,
            receiver=self.owner_id,
            elster_index=self.elster_index,
            value=round(value.value / self.factor),
        )


RegisterDefinition = Union[
    NumberSensorRegisterDefinition, NumberSettingRegisterDefinition
]

SensorRegisterDefinition = Union[NumberSensorRegisterDefinition]

SettingRegisterDefinition = Union[NumberSettingRegisterDefinition]
