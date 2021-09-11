import asyncio
from typing import AsyncIterable, cast

import can

from ..elster_protocol.elster_frame import ElsterFrame
from ..elster_protocol.parse_can_message import parse_can_message
from ..utils.publish_subscribe_topic import PublishSubscribeTopic
from ..utils.stopping import stopping


async def read_elster_canbus(topic: PublishSubscribeTopic[ElsterFrame], bus: can.Bus):
    reader = can.AsyncBufferedReader()

    with stopping(
        can.Notifier(bus=bus, listeners=[reader], loop=asyncio.get_event_loop())
    ):
        async for message in cast(AsyncIterable[can.Message], reader):
            elster_frame = parse_can_message(message)
            topic.publish(elster_frame)
