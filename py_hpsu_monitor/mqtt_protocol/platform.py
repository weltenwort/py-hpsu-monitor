from typing import Literal, Union

from ..elster_protocol.register_types import (
    BaseRegisterDefinition,
    NumberSettingRegisterDefinition,
)

Platform = Union[Literal["sensor"], Literal["number"]]


def get_platform(register_definition: BaseRegisterDefinition) -> Platform:
    if isinstance(register_definition, NumberSettingRegisterDefinition):
        return "number"
    else:
        return "sensor"
