from typing import Generic, TypeVar, Callable, Coroutine
import asyncio
from ..async_lib.TaskQueue import TaskQueue

T = TypeVar('T')


class ScheduleMethod:
    __slots__ = 'routetine', 'task_queue'
    def __init__(self, callable: Callable, task_queue: TaskQueue):
        self.callable: Callable = callable
        self.task_queue: TaskQueue = task_queue

    def call(self, *args, **kargs):
        return self.task_queue.schedule(asyncio.create_task(self.callable(**kargs)))


class SingleFunctionSchedule(Generic[T, R]):
    def __init__(self, callable: Callable[[T], R], task_queue: TaskQueue):
        self.method = ScheduleMethod(callable, task_queue)

    def call(self, value: T) -> R:
        return self.method.call(value)



class SingleFunction(Generic[T, R]):
    def __init__(self, callable: Callable[[T], R], schedule: SingleConsumerSchedule[T, R]):
        self.callable: Callable[[T], R] = callable
        self.routine: Coroutine[T, R] = routine

    def call(self, value: T):
        if self.callable is not None:
            self.callable(value)
        elif self.schedule.call(value)


CallOnError = SingleConsumer[Exception]


class Function():
    def __init__(self, callable: Callable[[], None], routine: Coroutine[None]):
        self.callable: Callable[[], None] = callable
        self.routine: Coroutine[[], None] = routine

    def call(self):
        if self.callable is not None:
            self.callable(value)
        elif self.routine is not None
CallOnCompleted = Union[Callable, Coroutine[None]]

