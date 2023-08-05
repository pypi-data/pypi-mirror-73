from typing import List, TypeVar, Generic, Callable, Union, Coroutine, Optional
from .BaseObservable import BaseObservable

T = TypeVar('T')


class Subscription(Generic[T]):
    def __init__(self, obs: BaseObservable[T], on_next: Callable[[T], None], on_error: Callable[[Exception], None], on_completed: Callable[[], None]):
        self.observable: BaseObservable[T] = obs
        self.on_next: Callable[[T], None] = on_next
        self.on_error: Callable[[Exception], None] = on_error
        self.on_completed: Callable[[], None] = on_completed
        self.is_close = False

    def call_on_next(self, value: T):
        if self.is_close == False and self.on_next is not None:
            self.on_next(value)

    def call_on_error(self, error: Exception):
        if self.is_close == False and self.on_error is not None:
            self.on_error(error)

    def call_on_completed(self):
        if self.is_close == False and self.on_completed is not None:
            self.on_completed(self)

    def close(self):
        self.is_close = True