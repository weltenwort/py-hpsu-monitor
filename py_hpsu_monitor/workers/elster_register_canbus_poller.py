import asyncio
from typing import Callable, List, cast

import can
from pydantic import BaseModel

from ..elster_protocol.create_can_message import create_can_message
from ..elster_protocol.elster_frame import ElsterReadRequestFrame
from ..elster_protocol.register_types import RegisterDefinition


async def poll_elster_registers_canbus(
    bus: can.Bus,
    polling_configurations: List["RegisterPollingConfiguration"],
    sender_id: int,
):
    await asyncio.gather(
        *[
            poll_elster_register(
                bus=bus,
                elster_index=polling_configuration.register_definition.elster_index,
                sender_id=sender_id,
                receiver_id=polling_configuration.register_definition.owner_id,
                interval=polling_configuration.interval,
                start_delay=float(index),
            )
            for index, polling_configuration in enumerate(polling_configurations)
            if polling_configuration.enabled
        ]
    )


async def poll_elster_register(
    bus: can.Bus,
    elster_index: int,
    sender_id: int,
    receiver_id: int,
    interval: float,
    start_delay: float = 0.0,
):
    await asyncio.sleep(start_delay)

    sendMessage = cast(Callable[[can.Message], None], bus.send)  # type: ignore

    while True:
        sendMessage(
            create_can_message(
                ElsterReadRequestFrame(
                    timestamp=0,
                    sender=sender_id,
                    receiver=receiver_id,
                    elster_index=elster_index,
                )
            )
        )
        await asyncio.sleep(interval)


class RegisterPollingConfiguration(BaseModel):
    register_definition: RegisterDefinition
    enabled: bool
    interval: float
