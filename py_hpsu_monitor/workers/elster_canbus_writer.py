from typing import Any, Callable, cast

import can

from ..elster_protocol.create_can_message import create_can_message
from ..elster_protocol.register_types import RegisterValue, WritableRegisterDefinition
from ..utils.publish_subscribe_topic import PublishSubscribeTopic


async def write_elster_canbus(
    written_register_values: PublishSubscribeTopic[
        RegisterValue[Any, WritableRegisterDefinition]
    ],
    bus: can.Bus,
    sender_id: int,
):
    sendMessage = cast(Callable[[can.Message], None], bus.send)  # type: ignore

    async for register_value in written_register_values.items():
        register_type = register_value.register_type
        frame = register_type.create_elster_write_frame(sender_id, register_value)

        sendMessage(create_can_message(frame))
