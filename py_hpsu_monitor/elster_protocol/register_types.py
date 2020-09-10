from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, TypeVar

from .elster_frame import ElsterReadResponseFrame

ValueType = TypeVar("ValueType")


@dataclass(frozen=True)
class RegisterValue:
    register_type: "RegisterDefinition"
    timestamp: float
    value: ValueType


@dataclass(frozen=True)
class RegisterDefinition:
    elster_index: int
    name: str
    description: Optional[str] = None
    label: Optional[str] = None

    @abstractmethod
    def parse_elster_frame(self, frame: ElsterReadResponseFrame):
        raise NotImplementedError


@dataclass(frozen=True)
class NumberRegisterDefinition(RegisterDefinition):
    factor: float = 1.0

    def parse_elster_frame(self, frame: ElsterReadResponseFrame):
        return RegisterValue(
            register_type=self,
            timestamp=frame.timestamp,
            value=frame.value * self.factor,
        )
