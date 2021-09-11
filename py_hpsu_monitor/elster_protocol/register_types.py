from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar, Union

from pydantic import BaseModel
from typing_extensions import Literal

from .elster_frame import ElsterReadResponseFrame

ValueType = TypeVar("ValueType")


@dataclass(frozen=True)
class RegisterValue(Generic[ValueType]):
    register_type: "RegisterDefinition"
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
    def parse_elster_frame(self, frame: ElsterReadResponseFrame) -> RegisterValue[Any]:
        raise NotImplementedError


class NumberRegisterDefinition(BaseRegisterDefinition):
    kind: Literal["number"] = "number"
    factor: float = 1.0
    unit: Optional[str] = None

    def parse_elster_frame(self, frame: ElsterReadResponseFrame):
        return RegisterValue(
            register_type=self,
            timestamp=frame.timestamp,
            value=frame.value * self.factor,
        )


RegisterDefinition = Union[NumberRegisterDefinition]
