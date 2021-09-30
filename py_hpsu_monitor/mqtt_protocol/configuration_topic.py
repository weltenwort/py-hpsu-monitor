import json
from py_hpsu_monitor.mqtt_protocol.write_topic import get_write_topic

from ..config import MqttConfig
from ..elster_protocol.register_types import (
    RegisterDefinition,
    WritableRegisterDefinition,
)
from .device import get_device_class
from .entity import get_entity_id
from .platform import get_platform
from .state_topic import get_state_topic


def get_configuration_topic(
    mqtt_config: MqttConfig, register_definition: RegisterDefinition
):
    return mqtt_config.configuration_topic_template.format(
        object_id=get_entity_id(mqtt_config, register_definition),
        platform=get_platform(register_definition),
    )


def get_configuration_payload(
    mqtt_config: MqttConfig, register_definition: RegisterDefinition
):
    sensor_name = get_entity_id(mqtt_config, register_definition)
    state_topic = get_state_topic(mqtt_config, register_definition)
    command_topic_attrs = (
        {"command_topic": get_write_topic(mqtt_config, register_definition)}
        if (isinstance(register_definition, WritableRegisterDefinition))
        else {}
    )
    return json.dumps(
        {
            **{
                "name": sensor_name,
                "state_topic": state_topic,
                "value_template": "{{ value_json.value }}",
                "device": {
                    "identifiers": [mqtt_config.device.id],
                    "manufacturer": mqtt_config.device.manufacturer,
                    "model": mqtt_config.device.model,
                    "name": mqtt_config.device.name,
                },
                "unique_id": sensor_name,
            },
            **command_topic_attrs,
            **get_device_class(register_definition),
        }
    )
