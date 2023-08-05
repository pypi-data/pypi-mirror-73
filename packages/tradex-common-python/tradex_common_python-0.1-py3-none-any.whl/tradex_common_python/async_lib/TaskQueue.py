import asyncio
import logging
from asyncio.queues import QueueEmpty

logger = logging.getLogger(__name__)
MINIMUM_DEBUG_LEVEL = 5
MAX_WARNING_LEVEL = 300
MAX_WARNING_LEVEL_TIMES = 100


class TaskQueue:
    def __init__(self, loop, no_running_task: int = 20, timeout_in_second: int = 5, log_task: bool = False):
        self.loop = loop
        self.queue: asyncio.Queue = asyncio.Queue(loop=self.loop)
        self.no_running_task: int = no_running_task
        self.started_tasks: int = 0
        self.warning_times: int = 0
        self.timeout_in_second: int = timeout_in_second
        self.log_task: bool = log_task

    def info(self):
        if self.started_tasks > MINIMUM_DEBUG_LEVEL:
            logger.debug('tasks: %s', self.started_tasks)
            if self.started_tasks > MAX_WARNING_LEVEL:
                self.warning_times += 1
                if self.warning_times >= MAX_WARNING_LEVEL_TIMES:
                    logger.warning('tasks: %s', self.started_tasks)
                    self.warning_times = 0
            else:
                self.warning_times = 0

    def schedule(self, task):
        task.name = ''
        self.queue.put_nowait(task)
        self.info()

    def schedule_w_name(self, task, name):
        task.name = name
        self.queue.put_nowait(task)
        self.info()

    async def do_task(self, queue, delay):
        while True:
            try:
                task: asyncio.Task = queue.get_nowait()
                self.started_tasks = self.started_tasks + 1
                try:
                    if self.log_task:
                        logger.info("running task:%s", task)
                    await asyncio.wait_for(task, self.timeout_in_second)
                except asyncio.CancelledError:
                    pass
                except asyncio.TimeoutError:
                    logger.error("timeout for current task: %s", task)
                self.started_tasks = self.started_tasks - 1
                self.info()
            except QueueEmpty:
                # logger.warning('queue delay %s', delay)
                await asyncio.sleep(delay)
            except Exception as error:
                logger.error('got error while running a task %s', error, exc_info=True)

    def run(self):
        tasks = []
        for i in range(self.no_running_task):
            tasks.append(self.do_task(self.queue, i))
        self.loop.run_until_complete(asyncio.wait(tasks))
