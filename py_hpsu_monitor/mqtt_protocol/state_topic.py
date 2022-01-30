import json
from typing import Any

from ..config import MqttConfig
from ..elster_protocol.register_types import (
    BaseRegisterDefinition,
    RegisterDefinition,
    RegisterValue,
)
from .entity import get_entity_id
from .platform import get_platform


def get_state_topic(
    mqtt_config: MqttConfig, register_definition: BaseRegisterDefinition
):
    return mqtt_config.state_topic_template.format(
        object_id=get_entity_id(mqtt_config, register_definition),
        platform=get_platform(register_definition),
    )


def get_state_payload(register_value: RegisterValue[Any, RegisterDefinition]):
    return json.dumps(
        {"timestamp": register_value.timestamp, "value": register_value.value}
    )
