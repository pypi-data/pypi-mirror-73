from confluent_kafka import Producer
from .Message import MessageType, Message
from .Consumer import AsyncConsumer
import asyncio
import simplejson as json
from ..utils.time import get_current_time_in_ms
import logging
from typing import Dict, Type, Union, Callable, Optional, Any
from ..async_lib.TaskQueue import TaskQueue
from ..models.Base import Base
import threading

logger = logging.getLogger(__name__)


def my_kafka_error(err):
    logger.warning("kafka global error: %s", err)


class BaseProducer():
    def __init__(self, conf: Dict, auto_set_time: bool = True):
        self.producer: Producer = Producer({
            'bootstrap.servers': 'mybroker1,mybroker2',
            'error_cb': my_kafka_error,
            **conf
        })
        self.auto_set_time: bool = auto_set_time
        self.poll_in_thread()
        logger.warning("initialized kafka producer: %s", conf)

    def send(self, topic: str, message: Union[Message, Dict], message_key: Optional[str]=None) -> None:
        if self.auto_set_time:
            if isinstance(message, dict):
                message['t'] = get_current_time_in_ms()
            elif isinstance(message, Message):
                message.t = get_current_time_in_ms()

        jsonMsg = json.dumps(message, ignore_nan=True)
        self.producer.produce(topic, jsonMsg, key=message_key, callback=self.delivery_report)
        logger.info('send to topic %s key %s: %s', topic, message_key, jsonMsg)
        self.poll_in_thread()

    def delivery_report(self, err, msg, silent=False):
        if err is not None:
            logger.error('fail to delivery message %s', err)
            return
        logger.info('msg delivered to {} [{}]: {}'.format(
            msg.topic(), msg.partition(), msg.value()))

    def poll_in_thread(self):
        th = threading.Thread(target=self.poll, daemon=True)
        th.start()

    def poll(self):
        nQueueMsgs = self.producer.flush(3)
        logger.warning("nQueueMsgs: %s", nQueueMsgs)


class CommonSender(BaseProducer):
    def __init__(self, conf: Dict, source_id: str, auto_set_time: bool = False):
        super(CommonSender, self).__init__(conf, auto_set_time)
        self.source_id: str = source_id
        self.message_id: int = 0

    def get_message_id(self) -> int:
        self.message_id += 1
        return self.message_id

    def send(self, tx_id: str, topic: str, uri: str, message_type: str, body, key: Optional[str]=None,
             response_topic: Optional[str]=None, response_uri: Optional[str]=None,
             message_id: Optional[Union[str, int]]=None):
        data = body
        if isinstance(data, Base):
            data = data.to_dict()
        elif hasattr(data, 'to_dict'):
            data = data.to_dict()

        msg_id = message_id if (message_id is not None) else self.get_message_id()
        super(CommonSender, self).send(topic, {
            "messageType": message_type,
            "sourceId": self.source_id,
            "messageId": msg_id,
            "transactionId": tx_id,
            "uri": uri,
            "responseDestination": None if response_topic is None else {
                "topic": response_topic,
                "uri": response_uri
            },
            "data": data,
        }, key if key is not None else str(msg_id))

    def send_message(self, tx_id: str, topic: str, uri: str, body, key: Optional[str]=None, message_id: Optional[Union[str, int]]=None):
        self.send(tx_id, topic, uri, MessageType.MESSAGE.value, body, key, None, None, message_id)

    def send_response(self, message: Message, body, key: Optional[str]=None):
        if message is not None and message.responseDestination is not None :
            self.send(message.transactionId, message.responseDestination.topic, message.responseDestination.uri, MessageType.RESPONSE.value, body, key, None, None, message.messageId)

    def forward_message(self, message: Message, new_topic: str, new_uri: str, key: Optional[str]=None):
        if message is not None and message.responseDestination is not None :
            self.send(message.transactionId, new_topic, new_uri, message.messageType, message.data, key, None, None, message.messageId)


class RequestSender(CommonSender):
    def __init__(self, conf: Dict, source_id: str, cluster_id: str, node_id: str):
        super(RequestSender, self).__init__(conf, source_id)
        self.fast_producer: CommonSender = CommonSender({
            **conf,
            "batch.num.messages": 5,
        }, source_id)
        self.response_topic: str = '{0}.response.{1}'.format(cluster_id, node_id)
        self.response_uri: str = ''
        self.cb_dict: Dict = dict()

    def get_response_topic(self) -> str:
        return self.response_topic

    async def reiceive_response(self, message: Message, key: str, error: Any, msg_string: str):
        try:
            if error is not None:
                logger.error('got error while listening respond %s', error, exc_info=True)
            if message.messageId in self.cb_dict:
                self.cb_dict[message.messageId]['cb'](message, key, error, msg_string)
            else:
                logger.warning('does not know where to response %s', message.messageId)
        except:
            logger.error('fail to handle response %s %s', msg_string, error)

    def send_request(self, tx_id: str, topic: str, uri: str, request, cb: Callable[[Message, str, Any, str], None], timeout: int, key: Optional[str]=None):
        msg_id = self.get_message_id()
        current_time = get_current_time_in_ms()
        self.cb_dict[msg_id] = {
            "cb": cb,
            "timeout": timeout,
            "time": current_time
        }
        self.fast_producer.send(tx_id, topic, uri, MessageType.REQUEST.value, request, None, self.response_topic, self.response_uri, msg_id)
        self.set_timeout(msg_id, current_time, timeout)

    def set_timeout(self, msg_id: str, current_time: int, timeout: int):
        pass


class AsyncRequestSender(RequestSender):
    def __init__(self, conf: Dict, source_id: str, cluster_id: str, node_id: str, task_queue: TaskQueue, consumer_conf: Optional[Dict]=None):
        super(AsyncRequestSender, self).__init__(conf, source_id, cluster_id, node_id)
        self.task_queue: TaskQueue = task_queue
        self.response_listener: AsyncConsumer = AsyncConsumer(task_queue, self.reiceive_response, [self.response_topic], consumer_conf if consumer_conf is not None else {
            'auto.offset.reset': 'earliest',
        })

    def set_timeout(self, msg_id: str, current_time: int, timeout: int):
        self.task_queue.schedule(asyncio.create_task(self.handle_timeout(msg_id, current_time, timeout)))

    async def handle_timeout(self, msg_id: str, current_time: int, timeout: int):
        await asyncio.sleep(timeout)
        if msg_id in self.cb_dict:
            self.task_queue.schedule(asyncio.create_task(self.cb_dict[msg_id]['cb'](None, None, 'timeout', None)))
            del self.cb_dict[msg_id]
