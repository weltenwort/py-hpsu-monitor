import asyncio
from typing import List

import can
from pydantic import BaseModel

from ..elster_protocol.create_can_message import create_can_message
from ..elster_protocol.elster_frame import ElsterReadRequestFrame


async def poll_elster_registers_canbus(
    bus: can.Bus,
    polling_configurations: List["RegisterPollingConfiguration"],
    sender_id: int,
):
    await asyncio.gather(
        *[
            poll_elster_register(
                bus=bus,
                polling_configuration=polling_configuration,
                sender_id=sender_id,
            )
            for polling_configuration in polling_configurations
        ]
    )


async def poll_elster_register(
    bus: can.Bus, polling_configuration: "RegisterPollingConfiguration", sender_id: int
):
    await asyncio.sleep(polling_configuration.start_delay)

    while True:
        bus.send(
            create_can_message(
                ElsterReadRequestFrame(
                    timestamp=0,
                    sender=sender_id,
                    receiver=polling_configuration.receiver_id,
                    elster_index=polling_configuration.elster_index,
                )
            )
        )
        await asyncio.sleep(polling_configuration.interval)


class RegisterPollingConfiguration(BaseModel):
    elster_index: int
    interval: float
    receiver_id: int
    start_delay: float = 0
