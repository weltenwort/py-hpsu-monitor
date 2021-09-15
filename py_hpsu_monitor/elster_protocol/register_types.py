from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Literal, Optional, TypeVar, Union

from pydantic import BaseModel

from .elster_frame import ElsterReadResponseFrame, ElsterWriteFrame

ValueType = TypeVar("ValueType")
RegisterDefinitionType = TypeVar(
    "RegisterDefinitionType", bound="BaseRegisterDefinition", covariant=True
)
NumberRegisterDefinitionType = TypeVar(
    "NumberRegisterDefinitionType", bound="NumberRegisterDefinition"
)


@dataclass(frozen=True)
class RegisterValue(Generic[ValueType, RegisterDefinitionType]):
    register_type: RegisterDefinitionType
    timestamp: float
    value: ValueType


class BaseRegisterDefinition(BaseModel, ABC):
    kind: str = "register"
    elster_index: int
    name: str
    owner_id: int

    class Config:
        allow_mutation = False

    @abstractmethod
    def parse_elster_frame(
        self, frame: ElsterReadResponseFrame
    ) -> RegisterValue[Any, Any]:
        raise NotImplementedError


class NumberRegisterDefinition(BaseRegisterDefinition, ABC):
    kind: Literal["number"] = "number"
    factor: float = 1.0
    unit: Optional[str] = None
    is_writable: bool = False

    def parse_elster_frame(self, frame: ElsterReadResponseFrame):
        return RegisterValue(
            register_type=self,
            timestamp=frame.timestamp,
            value=frame.value * self.factor,
        )


class ReadonlyNumberRegisterDefinition(NumberRegisterDefinition):
    is_writable: Literal[False] = False


class WritableNumberRegisterDefinition(NumberRegisterDefinition):
    is_writable: Literal[True] = True

    def create_elster_write_frame(
        self,
        sender_id: int,
        value: RegisterValue[float, "WritableNumberRegisterDefinition"],
    ):
        return ElsterWriteFrame(
            timestamp=value.timestamp,
            sender=sender_id,
            receiver=self.owner_id,
            elster_index=self.elster_index,
            value=round(value.value / self.factor),
        )


RegisterDefinition = Union[
    ReadonlyNumberRegisterDefinition, WritableNumberRegisterDefinition
]

WritableRegisterDefinition = Union[WritableNumberRegisterDefinition]
