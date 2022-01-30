from asyncio import gather
from typing import Any, AsyncContextManager, AsyncGenerator, List, cast

import asyncio_mqtt
from loguru import logger
from paho.mqtt.client import MQTTMessage
from pydantic import ValidationError

from ..config import MqttConfig
from ..elster_protocol.register_types import (
    RegisterDefinition,
    RegisterValue,
    WritableRegisterDefinition,
)
from ..mqtt_protocol.write_topic import get_overall_write_topic, get_write_topic
from ..utils.publish_subscribe_topic import PublishSubscribeTopic


async def mqtt_listen_for_elster_registers(
    written_register_values: PublishSubscribeTopic[
        RegisterValue[Any, WritableRegisterDefinition]
    ],
    mqtt_client: asyncio_mqtt.Client,
    mqtt_config: MqttConfig,
    register_definitions: List[RegisterDefinition],
):
    writable_register_definitions = [
        register_definition
        for register_definition in register_definitions
        if isinstance(register_definition, WritableRegisterDefinition)
    ]

    write_topic = get_overall_write_topic(mqtt_config)

    await gather(
        *[
            mqtt_listen_for_elster_register(
                written_register_values=written_register_values,
                mqtt_client=mqtt_client,
                mqtt_config=mqtt_config,
                register_definition=register_definition,
            )
            for register_definition in writable_register_definitions
        ],
        mqtt_client.subscribe(write_topic)
    )


async def mqtt_listen_for_elster_register(
    written_register_values: PublishSubscribeTopic[
        RegisterValue[Any, WritableRegisterDefinition]
    ],
    mqtt_client: asyncio_mqtt.Client,
    mqtt_config: MqttConfig,
    register_definition: WritableRegisterDefinition,
):
    write_topic = get_write_topic(
        mqtt_config=mqtt_config, register_definition=register_definition
    )

    filtered_messages = cast(
        AsyncContextManager[AsyncGenerator[MQTTMessage, None]],
        mqtt_client.filtered_messages(write_topic),
    )

    async with filtered_messages as messages:
        async for message in messages:
            with logger.catch(ValidationError):
                value = register_definition.parse_mqtt_write_message(message)

            with logger.catch():
                written_register_values.publish(value)
