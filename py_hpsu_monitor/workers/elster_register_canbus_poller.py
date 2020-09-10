import asyncio
from typing import List

import can
from typing_extensions import TypedDict

from ..elster_protocol.create_can_message import create_can_message
from ..elster_protocol.elster_frame import ElsterReadRequestFrame


async def poll_elster_registers_canbus(
    bus: can.Bus, polling_configurations: List["RegisterPollingConfiguration"]
):
    await asyncio.gather(
        *[
            poll_elster_register(bus=bus, polling_configuration=polling_configuration)
            for polling_configuration in polling_configurations
        ]
    )


async def poll_elster_register(
    bus: can.Bus, polling_configuration: "RegisterPollingConfiguration"
):
    while True:
        bus.send(
            create_can_message(
                ElsterReadRequestFrame(
                    timestamp=0,
                    sender=polling_configuration["sender"],
                    receiver=polling_configuration["receiver"],
                    elster_index=polling_configuration["elster_index"],
                )
            )
        )
        await asyncio.sleep(polling_configuration["interval"])


class RegisterPollingConfiguration(TypedDict):
    elster_index: int
    interval: float
    receiver: int
    sender: int
