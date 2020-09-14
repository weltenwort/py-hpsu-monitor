import asyncio
from typing import List, Optional

import can
from pydantic import BaseModel

from ..elster_protocol.create_can_message import create_can_message
from ..elster_protocol.elster_frame import ElsterReadRequestFrame
from ..elster_protocol.register_definitions import group_register_definitions_by_index
from ..elster_protocol.register_types import RegisterDefinition


async def poll_elster_registers_canbus(
    bus: can.Bus,
    polling_configurations: List["RegisterPollingConfiguration"],
    register_definitions: List[RegisterDefinition],
    sender_id: int,
):
    register_definitions_by_index = group_register_definitions_by_index(
        register_definitions
    )
    print(register_definitions_by_index)

    for polling_configuration in polling_configurations:
        if polling_configuration.elster_index not in register_definitions_by_index:
            raise UnkownElsterIndexError(
                elster_index=polling_configuration.elster_index
            )

    await asyncio.gather(
        *[
            poll_elster_register(
                bus=bus,
                polling_configuration=polling_configuration,
                sender_id=sender_id,
                receiver_id=register_definitions_by_index[
                    polling_configuration.elster_index
                ].owner_id,
            )
            for polling_configuration in polling_configurations
        ]
    )


async def poll_elster_register(
    bus: can.Bus,
    polling_configuration: "RegisterPollingConfiguration",
    sender_id: int,
    receiver_id: int,
):
    await asyncio.sleep(polling_configuration.start_delay)

    while True:
        bus.send(
            create_can_message(
                ElsterReadRequestFrame(
                    timestamp=0,
                    sender=sender_id,
                    receiver=receiver_id,
                    elster_index=polling_configuration.elster_index,
                )
            )
        )
        await asyncio.sleep(polling_configuration.interval)


class RegisterPollingConfiguration(BaseModel):
    elster_index: int
    interval: float
    start_delay: float = 0.0


class UnkownElsterIndexError(Exception):
    def __init__(self, elster_index: int, message: Optional[str] = None):
        self.elster_index = elster_index
        self.message = message or f"Failed to find elster index 0x{elster_index:04x}"

        super().__init__(self.message)
