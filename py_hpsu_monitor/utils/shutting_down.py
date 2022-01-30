from abc import abstractmethod
from contextlib import contextmanager
from typing import Generator, TypeVar

from typing_extensions import Protocol


class SupportsShutdown(Protocol):
    @abstractmethod
    def shutdown(self) -> None:
        raise NotImplementedError


SupportsShutdownType = TypeVar("SupportsShutdownType", bound=SupportsShutdown)


@contextmanager
def shutting_down(
    subject: SupportsShutdownType,
) -> Generator[SupportsShutdownType, None, None]:
    try:
        yield subject
    finally:
        subject.shutdown()
