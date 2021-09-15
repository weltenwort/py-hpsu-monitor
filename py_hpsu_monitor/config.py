from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel
import tomlkit


def load_default_configuration():
    return PyHpsuMonitorConfig()


def load_configuration_from_file_path(config_file_path: Path):
    if not config_file_path.is_file():
        return load_default_configuration()

    return load_configuration_from_text(config_file_path.read_text())


def load_configuration_from_text(config_file_text: str) -> "PyHpsuMonitorConfig":
    return PyHpsuMonitorConfig.parse_obj(dict(tomlkit.parse(config_file_text)))


class DefaultRegisterConfiguration(BaseModel):
    polling_enabled: bool = True
    polling_interval: float = 60.0


class RegisterConfiguration(BaseModel):
    elster_index: int
    polling_enabled: Optional[bool]
    polling_interval: Optional[float]


class CanBusConfig(BaseModel):
    sender_id: int = 0x680
    default_register_configuration: DefaultRegisterConfiguration = (
        DefaultRegisterConfiguration()
    )
    register_configuration: List[RegisterConfiguration] = []

    class Config:
        allow_mutation = False


class MqttBrokerConfig(BaseModel):
    hostname: str = "localhost"
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None


class MqttDeviceConfig(BaseModel):
    id: str = "hpsu-0"
    name: str = "HPSU 0"
    manufacturer: str = "Rotex"
    model: str = "Unknown Model"


class MqttConfig(BaseModel):
    enabled: bool = True
    configuration_topic_template: str = "homeassistant/{platform}/{object_id}/config"
    state_topic_template: str = "homeassistant/{platform}/{object_id}/state"
    write_topic_template: str = "homeassistant/{platform}/{device_id}/write"

    broker: MqttBrokerConfig = MqttBrokerConfig()
    device: MqttDeviceConfig = MqttDeviceConfig()


class PyHpsuMonitorConfig(BaseModel):
    can_bus: CanBusConfig = CanBusConfig()
    mqtt: MqttConfig = MqttConfig()

    class Config:
        allow_mutation = False
