import asyncio

from ..workers.elster_canbus_reader import read_elster_canbus
from ..workers.elster_frame_logger import log_elster_frames
from ..workers.elster_register_logger import log_elster_registers
from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..elster_protocol.elster_frame import ElsterFrame


async def run_monitor_canbus(log_frames: bool = False, log_registers: bool = False):
    elster_frames = PublishSubscribeTopic()  # type: PublishSubscribeTopic[ElsterFrame]

    await asyncio.gather(
        log_elster_frames(elster_frames) if log_frames else async_noop(),
        log_elster_registers(elster_frames) if log_registers else async_noop(),
        read_elster_canbus(elster_frames),
    )


async def async_noop():
    pass
