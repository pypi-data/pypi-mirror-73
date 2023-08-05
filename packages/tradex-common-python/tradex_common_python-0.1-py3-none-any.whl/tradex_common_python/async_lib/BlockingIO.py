import asyncio
from asyncio.futures import Future
from concurrent.futures import ThreadPoolExecutor, Future as CFuture
from typing import Callable, Any, Optional

from .TaskQueue import TaskQueue
from ..utils.time import get_current_time_in_ms

executor: ThreadPoolExecutor = None


def init(exec: ThreadPoolExecutor):
    global executor
    executor = exec if exec is not None else ThreadPoolExecutor(max_workers=30)


def get_executor() -> ThreadPoolExecutor:
    global executor
    if executor is None:
        executor = ThreadPoolExecutor(max_workers=30)
    return executor


def call_io(task_queue: TaskQueue, future: Future, callback: Callable[[Any, Exception], None], call: Callable, *args,
            **kargs):
    future: CFuture = get_executor().submit(call, *args, **kargs)
    task_queue.schedule_w_name(asyncio.create_task(check_result(future, task_queue, callback)), "check_result_call_io")


async def check_result(future: CFuture, task_queue: TaskQueue, callback: Callable[[Any, Exception], None],
                       time: Optional[int] = None):
    start_time: int = time if time is not None else get_current_time_in_ms()
    if future.done():
        try:
            callback(future.result(), None)
        except Exception as error:
            callback(None, error)
    else:
        task_queue.schedule_w_name(asyncio.create_task(check_result(future, task_queue, callback, start_time)),
                                   "check_result")


def io_callback(data: Any, error: Exception, fut: Future):
    if error is not None:
        fut.set_exception(error)
    else:
        fut.set_result(data)
