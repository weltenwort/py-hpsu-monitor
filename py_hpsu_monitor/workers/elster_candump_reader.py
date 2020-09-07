import can

from ..elster_protocol.elster_frame import ElsterFrame
from ..elster_protocol.parse_can_message import parse_can_message
from ..utils.publish_subscribe_topic import PublishSubscribeTopic


async def read_elster_candump(topic: PublishSubscribeTopic[ElsterFrame]):
    log_reader = can.CanutilsLogReader("contrib/candump-2020-09-05_135811.log")

    for message in log_reader:
        elster_frame = parse_can_message(message)
        topic.publish(elster_frame)
