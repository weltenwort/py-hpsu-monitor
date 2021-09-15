# pyright: reportUnnecessaryIsInstance=warning
from typing import List

import asyncio_mqtt

from ..config import MqttConfig
from ..elster_protocol.elster_frame import ElsterFrame, ElsterReadResponseFrame
from ..elster_protocol.register_definitions import group_register_definitions_by_index
from ..elster_protocol.register_types import (
    RegisterDefinition,
)
from ..mqtt_protocol.configuration_topic import (
    get_configuration_payload,
    get_configuration_topic,
)
from ..mqtt_protocol.state_topic import get_state_payload, get_state_topic
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
            topic=configuration_topic, payload=configuration_payload, retain=True
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

            await mqtt_client.publish(
                topic=state_topic, payload=state_payload, retain=True
            )
