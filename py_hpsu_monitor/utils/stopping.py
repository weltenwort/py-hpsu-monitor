from abc import abstractmethod
from contextlib import contextmanager
from typing import Protocol


class SupportsStop(Protocol):
    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError


@contextmanager
def stopping(subject: SupportsStop):
    try:
        yield subject
    finally:
        subject.stop()
