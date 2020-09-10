import asyncio
from typing import List

import can

from ..elster_protocol.elster_frame import ElsterFrame
from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..utils.shutting_down import shutting_down
from ..workers.elster_canbus_reader import read_elster_canbus
from ..workers.elster_frame_logger import log_elster_frames
from ..workers.elster_register_logger import log_elster_registers
from ..workers.elster_register_canbus_poller import (
    poll_elster_registers_canbus,
    RegisterPollingConfiguration,
)


async def run_monitor_canbus(
    can_interface: str,
    log_frames: bool = False,
    log_registers: bool = False,
    polling_configurations: List[RegisterPollingConfiguration] = [],
):
    elster_frames = PublishSubscribeTopic()  # type: PublishSubscribeTopic[ElsterFrame]

    with shutting_down(
        can.Bus(channel=can_interface, bustype="socketcan", receive_own_messages=True)
    ) as bus:
        await asyncio.gather(
            log_elster_frames(topic=elster_frames) if log_frames else async_noop(),
            log_elster_registers(topic=elster_frames)
            if log_registers
            else async_noop(),
            read_elster_canbus(topic=elster_frames, bus=bus),
            poll_elster_registers_canbus(
                bus=bus,
                polling_configurations=polling_configurations,
            ),
        )


async def async_noop():
    pass
