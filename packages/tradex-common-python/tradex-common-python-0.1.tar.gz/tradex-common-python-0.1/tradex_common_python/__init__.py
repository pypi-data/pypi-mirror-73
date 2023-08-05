from .kafka import Consumer, Message, Producer, RequestHandler
from .async_lib import TaskQueue
from .utils.log import init_log_to_console, init_log_by_config_file, \
    init_log_to_file, log_level, logger, ApplyOnRootLogger, LogConfig
# from .kafka.Consumer import AsyncConsumer
# from .async_lib.TaskQueue import TaskQueue
# import asyncio


# async def consumer_cb(msg, err):
#     if msg is not None:
#         print('callback')
#     else:
#         print('error consume')

# def real_rest_consumer():
#     loop = asyncio.get_event_loop()
#     task_queue = TaskQueue(loop, 3)
#     consumer = AsyncConsumer(task_queue, consumer_cb, ['test'], {
#         'bootstrap.servers': 'localhost:9092',
#         'group.id': 'test',
#     })
#     task_queue.schedule(loop.create_task(consumer.start_consume()))
#     task_queue.run()


# def test_consumer():
#     real_rest_consumer()
