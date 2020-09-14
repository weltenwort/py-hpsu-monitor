from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, TypeVar, Union

from pydantic import BaseModel
from typing_extensions import Literal

from .elster_frame import ElsterReadResponseFrame

ValueType = TypeVar("ValueType")


@dataclass(frozen=True)
class RegisterValue:
    register_type: "BaseRegisterDefinition"
    timestamp: float
    value: ValueType


class BaseRegisterDefinition(BaseModel, ABC):
    kind: Literal["register"] = "register"
    elster_index: int
    name: str
    owner_id: int

    class Config:
        allow_mutation = False

    @abstractmethod
    def parse_elster_frame(self, frame: ElsterReadResponseFrame) -> RegisterValue:
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
