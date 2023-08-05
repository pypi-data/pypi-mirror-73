import asyncio
import simplejson as json
import logging
from typing import List, Dict, Callable, Any, Awaitable, Optional, Union, Tuple

from confluent_kafka import Consumer, KafkaError, Message as ConfluentMessage
from confluent_kafka.cimpl import TIMESTAMP_CREATE_TIME, TIMESTAMP_LOG_APPEND_TIME

from .Message import Message, create_from_dict
from ..async_lib.TaskQueue import TaskQueue

logger = logging.getLogger(__name__)


class BaseConsumer:
    def __init__(self, topics: List[str], conf: Dict):
        self.consumer: Consumer = Consumer({
            'bootstrap.servers': None,
            'group.id': None,
            'auto.offset.reset': 'earliest',
            **conf
        })
        self.topics: List[str] = topics
        self.topic_dict: Dict[str, int] = dict((k, 1) for k in self.topics)
        self.consumer.subscribe(topics)

    # untested
    def subscribe(self, topics: List[str]):
        real_topics: List[str] = []
        for topic in topics:
            if topic not in self.topic_dict:
                real_topics.append(topic)
                self.topic_dict[topic] = 1
        self.consumer.subscribe(real_topics)

    def unsubscribe(self):
        self.consumer.unsubscribe()

    def consume(self, timeout: float = 0.1) -> Optional[ConfluentMessage]:
        return self.consumer.poll(timeout)


Callback = Callable[[Union[Message, None], Union[str, None], Any, Optional[str], Optional[int]], Awaitable[None]]

PAUSE_OFF: int = 0
PAUSE_ON: int = 1


class AsyncConsumer(BaseConsumer):
    def __init__(self, task_queue: TaskQueue, callback: Callback, topics: List[str], conf: Dict):
        super(AsyncConsumer, self).__init__(topics, conf)
        self.callback: Callback = callback
        self.task_queue: TaskQueue = task_queue
        self.is_pause: int = PAUSE_OFF

    def pause(self):
        logger.info("set pause flag is true")
        self.is_pause = PAUSE_ON

    def resume(self):
        self.is_pause = PAUSE_OFF
        logger.info("set pause flag is false")
        self.task_queue.schedule_w_name(asyncio.create_task(self.start_consume()), "consume kafka")

    async def start_consume(self):
        message: ConfluentMessage = self.consume()
        try:
            if message is not None:
                error = message.error()
                if error is not None:
                    if not error.code() == KafkaError._PARTITION_EOF:
                        pass
                    else:
                        self.task_queue.schedule_w_name(asyncio.create_task(self.callback(None, None, error, None, None)),
                                                        "callback kafka")
                else:
                    content: str = message.value()
                    content_dict = json.loads(content)
                    timestamp: Tuple[int, int] = message.timestamp()
                    creation_time: int = None
                    if timestamp is not None and (timestamp[0] == TIMESTAMP_CREATE_TIME or
                                                  timestamp[0] == TIMESTAMP_LOG_APPEND_TIME):
                        creation_time = timestamp[1]
                    msg: Message = create_from_dict(content_dict)
                    logger.info("handling message '%s'", content)
                    self.task_queue.schedule_w_name(asyncio.create_task(
                        self.callback(msg, message.key(), None, content, creation_time)), "callback kafka")
        except Exception as err:
            logger.error('handling message error %s %s', str(message.value()), str(err), exc_info=True)
        if self.is_pause == PAUSE_OFF:
            self.task_queue.schedule_w_name(asyncio.create_task(self.start_consume()), "consume kafka")
        else:
            logger.info("pause flag is true. Stop consuming")
