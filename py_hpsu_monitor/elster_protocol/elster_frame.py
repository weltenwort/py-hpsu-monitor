from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Literal, Union


class ElsterFrameType(IntEnum):
    READ_REQUEST = 1
    READ_RESPONSE = 2


@dataclass(frozen=True)
class ElsterBaseFrame:
    timestamp: float
    sender: int
    receiver: int

    def __repr__(self):
        return (
            f"ElsterBaseFrame("
            f"timestamp={datetime.utcfromtimestamp(self.timestamp)}, "
            f"sender={self.sender:x}, "
            f"receiver={self.receiver:x}, "
            ")"
        )


@dataclass(frozen=True)
class ElsterGenericFrame(ElsterBaseFrame):
    payload: bytes
    frame_type: int

    def __repr__(self):
        return (
            f"ElsterGenericFrame("
            f"timestamp={datetime.utcfromtimestamp(self.timestamp)}, "
            f"sender={self.sender:x}, "
            f"receiver={self.receiver:x}, "
            f"frame_type={self.frame_type}, "
            f"payload={self.payload}"
            ")"
        )


@dataclass(frozen=True)
class ElsterReadRequestFrame(ElsterBaseFrame):
    elster_index: int
    frame_type: Literal[ElsterFrameType.READ_REQUEST] = ElsterFrameType.READ_REQUEST

    def __repr__(self):
        return (
            f"ElsterReadRequestFrame("
            f"timestamp={datetime.utcfromtimestamp(self.timestamp)}, "
            f"sender={self.sender:x}, "
            f"receiver={self.receiver:x}, "
            f"elster_index={self.elster_index:04x}, "
            ")"
        )


@dataclass(frozen=True)
class ElsterReadResponseFrame(ElsterBaseFrame):
    elster_index: int
    value: int
    frame_type: Literal[ElsterFrameType.READ_RESPONSE] = ElsterFrameType.READ_RESPONSE

    def __repr__(self):
        return (
            f"ElsterReadResponseFrame("
            f"timestamp={datetime.utcfromtimestamp(self.timestamp)}, "
            f"sender={self.sender:x}, "
            f"receiver={self.receiver:x}, "
            f"elster_index={self.elster_index:04x}, "
            f"value={self.value:04x} ({self.value}), "
            ")"
        )


ElsterFrame = Union[ElsterReadRequestFrame, ElsterReadResponseFrame, ElsterGenericFrame]
