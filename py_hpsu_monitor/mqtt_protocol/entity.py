from ..config import MqttConfig
from ..elster_protocol.register_types import (
    BaseRegisterDefinition,
)


def get_entity_id(mqtt_config: MqttConfig, register_definition: BaseRegisterDefinition):
    return f"{mqtt_config.device.id}-{register_definition.name}"
