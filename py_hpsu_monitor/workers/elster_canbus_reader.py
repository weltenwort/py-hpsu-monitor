import asyncio

import can

from ..elster_protocol.elster_frame import ElsterFrame
from ..elster_protocol.parse_can_message import parse_can_message
from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..utils.shutting_down import shutting_down
from ..utils.stopping import stopping


async def read_elster_canbus(topic: PublishSubscribeTopic[ElsterFrame]):
    with shutting_down(
        can.Bus("vcan0", bustype="socketcan", receive_own_messages=True)
    ) as bus:
        reader = can.AsyncBufferedReader()

        with stopping(can.Notifier(bus, [reader], loop=asyncio.get_event_loop())):
            async for message in reader:
                elster_frame = parse_can_message(message)
                topic.publish(elster_frame)
