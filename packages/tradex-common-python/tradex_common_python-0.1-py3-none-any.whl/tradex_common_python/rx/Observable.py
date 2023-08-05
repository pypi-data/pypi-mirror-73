from typing import List, TypeVar, Generic, Callable, Union, Coroutine, Optional
from enum import Enum
from .BaseObservable import BaseObservable
from .Subscription import Subscription

T = TypeVar('T')


class PostitionType(Enum):
    EARLIEST = 0    # only receive new value
    LATEST = 1      # receive all value
    LAST = 2        # always receive latest value


class Observable(BaseObservable[T]):
    def __init__(self, position_type: Optional[int]=PostitionType.EARLIEST, value: Optional[T]=None, values: Optional[List[T]]=None):
        self.position_type: int = position_type
        if self.position_type > PostitionType.LAST and self.position_type < PostitionType.EARLIEST:
            self.position_type = PostitionType.EARLIEST
        self.subscriptions: List[Subscription[T]] = []
        self.values: List[T] = []

    def subscribe(self, on_next: Callable[[T], None], on_error: Callable[[Exception], None], on_completed: Callable[[], None]) -> Subscription:
        subscription: Subscription[T] = Subscription(self, on_next, on_error, on_completed)
        self.subscriptions.append(subscription)
        return subscription

    def next(self, value: T):
        self.values.append(value)
        for subscription in self.subscriptions:
            try:
                subscription.call_on_next(value)
            except Exception as err:
                subscription.call_on_error(err)
                subscription.close()

    def error(self, err: Exception):
        for subscription in self.subscriptions:
            subscription.call_on_error(err)
            subscription.observable = None
        self.values = None
        self.subscriptions = None

    def complete(self):
        for subscription in self.subscriptions:
            subscription.call_on_completed()
            subscription.observable = None
        self.values = None
        self.subscriptions = None

