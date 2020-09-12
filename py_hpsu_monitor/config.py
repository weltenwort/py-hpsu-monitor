from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, SecretStr
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


class MqttBrokerConfig(BaseModel):
    hostname: str = "localhost"
    port: int = 1883
    username: Optional[str] = None
    password: Optional[SecretStr] = None


class MqttConfig(BaseModel):
    configuration_topic_template: str = "homeassistant/sensor/{device_id}/config"
    state_topic_template: str = "homeassistant/sensor/{device_id}/state"
    device_id: str = "hpsu-0"

    broker: MqttBrokerConfig = MqttBrokerConfig()


class PyHpsuMonitorConfig(BaseModel):
    can_bus: CanBusConfig = CanBusConfig()
    mqtt: MqttConfig = MqttConfig()

    class Config:
        allow_mutation = False
