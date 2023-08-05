import uuid
from ..kafka.Consumer import AsyncConsumer
from ..kafka.Producer import AsyncRequestSender
from ..async_lib.TaskQueue import TaskQueue
from typing import Dict

class RequestHandlerTest:
    def __init__(self, task_queue: TaskQueue, consumer_conf: Dict, producer_conf: Dict):
        self.test_name = str(uuid.uuid4())
        self.tx_id = 0
        self.request_sender = AsyncRequestSender(producer_conf, 'tets', 'test', self.test_name, task_queue, consumer_conf)

    def get_tx_id(self):
        self.tx_id += 1
        return '{}'.format(self.tx_id)

    def send_request(self, topic, uri, body, cb):
        self.request_sender.send_request(self.get_tx_id(), topic, uri, body, cb, 3000)

class SimpleRequestHandlerTest(RequestHandlerTest):
    def __init__(self, task_queue: TaskQueue, kafka_url: str):
        super(SimpleRequestHandlerTest, self).__init__(task_queue, {
            'bootstrap.servers': kafka_url,
            'group.id': 'test',
        }, {
            'bootstrap.servers': kafka_url,
            "batch.num.messages": 5,
        })