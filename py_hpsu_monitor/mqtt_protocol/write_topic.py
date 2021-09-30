from ..config import MqttConfig
from ..elster_protocol.register_types import WritableRegisterDefinition
from .entity import get_entity_id
from .platform import get_platform


def get_overall_write_topic(mqtt_config: MqttConfig):
    return mqtt_config.write_topic_template.format(object_id="+", platform="+")


def get_write_topic(
    mqtt_config: MqttConfig, register_definition: WritableRegisterDefinition
):
    return mqtt_config.write_topic_template.format(
        object_id=get_entity_id(mqtt_config, register_definition),
        platform=get_platform(register_definition),
    )
