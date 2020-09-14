import json
from typing import List

import asyncio_mqtt

from ..config import MqttConfig
from ..elster_protocol.elster_frame import ElsterFrame, ElsterReadResponseFrame
from ..elster_protocol.register_definitions import group_register_definitions_by_index
from ..elster_protocol.register_types import (
    NumberRegisterDefinition,
    RegisterDefinition,
    RegisterValue,
)
from ..utils.publish_subscribe_topic import PublishSubscribeTopic


async def mqtt_log_elster_registers(
    elster_frames: PublishSubscribeTopic[ElsterFrame],
    mqtt_client: asyncio_mqtt.Client,
    mqtt_config: MqttConfig,
    register_definitions: List[RegisterDefinition],
):
    register_definitions_by_index = group_register_definitions_by_index(
        register_definitions
    )

    for register_definition in register_definitions:
        configuration_topic = get_configuration_topic(mqtt_config, register_definition)
        configuration_payload = get_configuration_payload(
            mqtt_config, register_definition
        )
        await mqtt_client.publish(
            topic=configuration_topic, payload=configuration_payload
        )

    async for frame in elster_frames.items():
        if (
            isinstance(frame, ElsterReadResponseFrame)
            and frame.elster_index in register_definitions_by_index
        ):
            register_value = register_definitions_by_index[
                frame.elster_index
            ].parse_elster_frame(frame)

            state_topic = get_state_topic(mqtt_config, register_value.register_type)
            state_payload = get_state_payload(register_value)

            await mqtt_client.publish(topic=state_topic, payload=state_payload)


def get_configuration_payload(
    mqtt_config: MqttConfig, register_definition: RegisterDefinition
):
    sensor_name = get_sensor_name(mqtt_config, register_definition)
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


def get_state_payload(register_value: RegisterValue):
    return json.dumps(
        {"timestamp": register_value.timestamp, "value": register_value.value}
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
    return f"{mqtt_config.device.id}-{register_definition.name}"


def get_device_class(register_definition: RegisterDefinition):
    if (
        isinstance(register_definition, NumberRegisterDefinition)
        and register_definition.unit
    ):
        device_class = device_class_by_unit.get(register_definition.unit, None)

        return {
            "unit_of_measurement": register_definition.unit,
            **(
                {
                    "device_class": device_class,
                }
                if device_class
                else {}
            ),
        }

    return {}


device_class_by_unit = {"°C": "temperature", "W": "power", "kW": "power"}
