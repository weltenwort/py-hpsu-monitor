import asyncio

from ..workers.elster_candump_reader import read_elster_candump
from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..elster_protocol.elster_frame import ElsterFrame


async def run_parse_candump():
    elster_frames = PublishSubscribeTopic()  # type: PublishSubscribeTopic[ElsterFrame]

    print_task = asyncio.create_task(print_frames(elster_frames))

    await asyncio.gather(
        # print_frames(elster_frames),
        elster_frames.join(),
        read_elster_candump(elster_frames),
    )

    print_task.cancel()


async def print_frames(topic: PublishSubscribeTopic[ElsterFrame]):
    async for frame in topic.items():
        print(frame)
