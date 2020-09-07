import asyncio

from ..workers.elster_canbus_reader import read_elster_canbus
from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..elster_protocol.elster_frame import ElsterFrame


async def run_monitor_canbus():
    elster_frames = PublishSubscribeTopic()  # type: PublishSubscribeTopic[ElsterFrame]

    await asyncio.gather(
        print_frames(elster_frames),
        read_elster_canbus(elster_frames),
    )


async def print_frames(topic: PublishSubscribeTopic[ElsterFrame]):
    async for frame in topic.items():
        print(frame)
