from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..elster_protocol.elster_frame import ElsterFrame


async def log_elster_frames(topic: PublishSubscribeTopic[ElsterFrame]):
    async for frame in topic.items():
        print(frame)
