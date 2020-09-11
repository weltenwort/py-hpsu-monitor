from pathlib import Path
from typing import List

from pydantic import BaseModel
import tomlkit

from .workers.elster_register_canbus_poller import RegisterPollingConfiguration


def load_default_configuration():
    return PyHpsuMonitorConfig()


def load_configuration_from_file_path(config_file_path: Path):
    if not config_file_path.is_file():
        return load_default_configuration()

    return load_configuration_from_text(config_file_path.read_text())


def load_configuration_from_text(config_file_text: str) -> "PyHpsuMonitorConfig":
    return PyHpsuMonitorConfig.parse_obj(dict(tomlkit.parse(config_file_text)))


class CanBusConfig(BaseModel):
    sender_id: int = 0x680
    polling_configuration: List[RegisterPollingConfiguration] = []

    class Config:
        allow_mutation = False


class PyHpsuMonitorConfig(BaseModel):
    can_bus: CanBusConfig = CanBusConfig()

    class Config:
        allow_mutation = False
