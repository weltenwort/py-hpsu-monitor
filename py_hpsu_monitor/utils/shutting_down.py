from abc import abstractmethod
from contextlib import contextmanager
from typing import Protocol


class SupportsShutdown(Protocol):
    @abstractmethod
    def shutdown(self) -> None:
        raise NotImplementedError


@contextmanager
def shutting_down(subject: SupportsShutdown):
    try:
        yield subject
    finally:
        subject.shutdown()
