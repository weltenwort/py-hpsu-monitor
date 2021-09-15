import json

from ..config import MqttConfig
from ..elster_protocol.register_types import RegisterDefinition
from .device import get_device_class
from .entity import get_entity_id
from .state_topic import get_state_topic


def get_configuration_topic(
    mqtt_config: MqttConfig, register_definition: RegisterDefinition
):
    return mqtt_config.configuration_topic_template.format(
        object_id=get_entity_id(mqtt_config, register_definition), platform="sensor"
    )


def get_configuration_payload(
    mqtt_config: MqttConfig, register_definition: RegisterDefinition
):
    sensor_name = get_entity_id(mqtt_config, register_definition)
    state_topic = get_state_topic(mqtt_config, register_definition)
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
            **get_device_class(register_definition),
        }
    )
