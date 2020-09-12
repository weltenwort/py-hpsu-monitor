import json

import asyncio_mqtt

from ..config import MqttConfig
from ..elster_protocol.elster_frame import ElsterFrame, ElsterReadResponseFrame
from ..elster_protocol.register_definitions import (
    register_definitions,
    register_definitions_by_index,
)
from ..elster_protocol.register_types import (
    NumberRegisterDefinition,
    RegisterDefinition,
)
from ..utils.publish_subscribe_topic import PublishSubscribeTopic


async def mqtt_log_elster_registers(
    elster_frames: PublishSubscribeTopic[ElsterFrame],
    mqtt_client: asyncio_mqtt.Client,
    mqtt_config: MqttConfig,
):
    for register_definition in register_definitions:
        configuration_topic = get_configuration_topic(mqtt_config, register_definition)
        configuration_payload = get_configuration_payload(
            mqtt_config, register_definition
        )
        await mqtt_client.publish(
            topic=configuration_topic, payload=configuration_payload
        )


def get_configuration_payload(
    mqtt_config: MqttConfig, register_definition: RegisterDefinition
):
    sensor_name = get_sensor_name(mqtt_config, register_definition)
    state_topic = get_state_topic(mqtt_config, register_definition)
    return json.dumps(
        {
            **{"name": sensor_name, "state_topic": state_topic},
            **(
                {"unit_of_measurement": register_definition.unit}
                if isinstance(register_definition, NumberRegisterDefinition)
                else {}
            ),
        }
    )


def get_configuration_topic(
    mqtt_config: MqttConfig, register_definition: RegisterDefinition
):
    return mqtt_config.configuration_topic_template.format(
        device_id=get_sensor_name(mqtt_config, register_definition)
    )


def get_state_topic(mqtt_config: MqttConfig, register_definition: RegisterDefinition):
    return mqtt_config.state_topic_template.format(
        device_id=get_sensor_name(mqtt_config, register_definition)
    )


def get_sensor_name(mqtt_config: MqttConfig, register_definition: RegisterDefinition):
    return f"{mqtt_config.device_id}-{register_definition.name}"
