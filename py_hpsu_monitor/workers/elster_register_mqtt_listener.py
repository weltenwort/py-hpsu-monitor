# pyright: reportUnnecessaryIsInstance=warning
from datetime import datetime
from typing import Any, AsyncContextManager, AsyncGenerator, List, cast

import asyncio_mqtt
from paho.mqtt.client import MQTTMessage

from ..config import MqttConfig
from ..elster_protocol.register_definitions import (
    group_register_definitions_by_name,
)
from ..elster_protocol.register_types import (
    RegisterDefinition,
    RegisterValue,
    WritableRegisterDefinition,
)
from ..mqtt_protocol.write_topic import get_write_topic, parse_write_payload
from ..utils.publish_subscribe_topic import PublishSubscribeTopic


async def mqtt_listen_for_elster_registers(
    written_register_values: PublishSubscribeTopic[
        RegisterValue[Any, WritableRegisterDefinition]
    ],
    mqtt_client: asyncio_mqtt.Client,
    mqtt_config: MqttConfig,
    register_definitions: List[RegisterDefinition],
):
    register_definitions_by_name = group_register_definitions_by_name(
        register_definitions
    )

    write_topic = get_write_topic(mqtt_config)
    filtered_messages = cast(
        AsyncContextManager[AsyncGenerator[MQTTMessage, None]],
        mqtt_client.filtered_messages(write_topic),
    )

    async with filtered_messages as messages:
        await mqtt_client.subscribe(write_topic)

        async for message in messages:
            payload = parse_write_payload(message.payload)
            register_definition = register_definitions_by_name.get(
                payload.register_name
            )

            if not isinstance(register_definition, WritableRegisterDefinition):
                continue  # TODO: log warning

            written_register_values.publish(
                RegisterValue(
                    register_type=register_definition,
                    timestamp=datetime.now().timestamp(),
                    value=payload.value,
                )
            )
