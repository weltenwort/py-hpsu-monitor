from abc import abstractmethod
from contextlib import contextmanager
from typing import Generator, TypeVar

from typing_extensions import Protocol


class SupportsStop(Protocol):
    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError


SupportsStopType = TypeVar("SupportsStopType", bound=SupportsStop)


@contextmanager
def stopping(subject: SupportsStopType) -> Generator[SupportsStopType, None, None]:
    try:
        yield subject
    finally:
        subject.stop()
