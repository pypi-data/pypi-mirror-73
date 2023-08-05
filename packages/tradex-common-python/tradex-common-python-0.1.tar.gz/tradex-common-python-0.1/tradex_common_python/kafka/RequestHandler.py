import asyncio
import logging
from asyncio import Future
from time import time
from typing import Union, Any, Callable, Optional, Dict

from tradex_common_python.utils.time import get_current_time_in_ms

from .Consumer import Consumer, AsyncConsumer
from .Message import Message
from .Producer import CommonSender
from ..async_lib.BlockingIO import check_result
from ..async_lib.TaskQueue import TaskQueue
from ..errors.GeneralError import GeneralError
from ..errors.UriNotFoundError import UriNotFoundError
from ..models.Response import Status, Response
from ..rx.Observable import Observable

logger = logging.getLogger(__name__)

ResultType = Union[Observable, bool, Future]
HandleType = Callable[[Message], ResultType]


class BaseRequestHandler():
    def __init__(self, producer: CommonSender, handle: HandleType):
        self.producer: CommonSender = producer
        self.producer.auto_set_time = True
        self.handle: Callable[[Message], ResultType] = handle

    def receive_message(self, message: Message, key: str, error: Any, str_message: Optional[str] = None):
        try:
            if error is not None:
                logger.error('error while receiving request %s', error)
                return
            start_time: float = time()
            try:
                result: ResultType = self.handle(message)
            except Exception as err:
                self.handle_error(message, key, err, str_message)
                return

            if result == True:
                logger.info("forward request %s took %s seconds", message.uri, time() - start_time)
                pass  # message is forwarded

            if result == False:
                self.handle_error(message, key, UriNotFoundError(), str_message)
            if isinstance(result, Observable):
                def on_receive_response(data):
                    self.producer.send_response(
                        message, Response(data, None).to_dict(), key
                    )
                    logger.info("handle request %s took %s seconds", message.uri, time() - start_time)

                def on_receive_error(error):
                    self.handle_error(message, key, error, str_message)
                    logger.info("handle request with error %s took %s seconds", message.uri, time() - start_time)

                result.subscribe(on_receive_response, on_receive_error, None)
            elif isinstance(result, Future):
                self.check_future_result(result, message, key, start_time, str_message)
            else:
                self.handle_error(message, key, GeneralError(), str_message)
        except Exception as err:
            self.handle_error(message, key, err, str_message)

    def check_future_result(self, fut: Future, message: Message, key: str, start_time: float, str_message: Optional[str] = None):
        result = fut.result()
        self.producer.send_response(message, Response(result, None).to_dict(), key)
        logger.info("handle request %s took %s seconds", message.uri, time() - start_time)

    def handle_error(self, message: Message, key: str, err: Exception, str_message: Optional[str]):
        status: Status = None
        logger.error('got error while processing request %s: %s', str_message, err, exc_info=True)
        if isinstance(err, GeneralError):
            status = err.get_status()
            if err.log_cb is not None:
                err.log_cb()
        else:
            status = GeneralError().set_source(err).get_status()
        self.producer.send_response(message, Response(None, status).to_dict(), key)


class AsyncRequestHandler(BaseRequestHandler):
    def __init__(self, handle: HandleType, cluster_id: str, task_queue: TaskQueue, producer: CommonSender = None,
                 consumer_conf: Optional[Dict] = {}, expired_in: int = 10000):
        self.listen_topic: str = cluster_id
        self.task_queue = task_queue
        self.consumer: Consumer = AsyncConsumer(task_queue, self.receive_request, [self.listen_topic], consumer_conf)
        self.expired_in: int = expired_in
        super(AsyncRequestHandler, self).__init__(producer, handle)

    async def receive_request(self, message: Message, key: str, error: Any, str_message: Optional[str], timestamp: Optional[int]):
        current_time_in_ms = get_current_time_in_ms()
        if timestamp is not None and timestamp > 0 and 0 < self.expired_in < current_time_in_ms - timestamp:
            logger.warning("ignore message since current time %s is larger than message time %s + expired_time %s",
                           current_time_in_ms, timestamp, self.expired_in)
        elif message.t is not None and message.t > 0 and 0 < self.expired_in < current_time_in_ms - message.t:
            logger.warning("ignore message since current time %s is larger than message time %s + expired_time %s",
                           current_time_in_ms, message.t, self.expired_in)
        else:
            self.receive_message(message, key, error, str_message)

    def check_future_result(self, fut: Future, message: Message, key: str, start_time: float, str_message: Optional[str] = None):
        callback: Callable[[Any, Exception], None] = \
            lambda data, error: self.receive_future_result(data, error, message, key, start_time, str_message)
        self.task_queue.schedule_w_name(asyncio.create_task(check_result(fut, self.task_queue, callback)),
                                        "check future result")

    def receive_future_result(self, result: Any, error: Exception, message: Message, key: str,
                              start_time: float, str_message: Optional[str] = None):
        if error is not None:
            self.handle_error(message, key, error, str_message)
        else:
            self.producer.send_response(message, Response(result, None).to_dict(), key)
        logger.info("handle request %s took %s seconds", message.uri, time() - start_time)
