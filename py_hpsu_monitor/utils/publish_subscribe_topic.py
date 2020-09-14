from asyncio import gather, Queue
from typing import Generic, Set, TypeVar


PublishSubscribeMessage = TypeVar("PublishSubscribeMessage")


class PublishSubscribeTopic(Generic[PublishSubscribeMessage]):
    def __init__(self):
        self.queues = set()  # type: Set[Queue[PublishSubscribeMessage]]

    def publish(self, message: PublishSubscribeMessage):
        for queue in self.queues:
            queue.put_nowait(message)

    async def join(self):
        await gather(*[queue.join() for queue in self.queues])

    async def items(self):
        queue: Queue[PublishSubscribeMessage] = Queue()
        self.queues.add(queue)

        try:
            while True:
                yield await queue.get()
                queue.task_done()
        finally:
            self.queues.remove(queue)
