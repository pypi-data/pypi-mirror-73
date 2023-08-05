from __future__ import annotations
from ..models.Response import Status, ParamError
from typing import Type, NewType, Optional, List, Dict, Any, Callable


class GeneralError(Exception):
    __slots__ = 'code', 'messageParams', 'params', 'source', 'log_cb'
    def __init__(self, code: Optional[str]='INTERNAL_SERVER_ERROR', messageParams: Optional[List[str]]=None, params: Optional[List[ParamError]]=None, source: Optional[Any]=None) -> None:
        self.code: str = code
        self.messageParams: Optional[List[str]] = messageParams
        self.params: Optional[List[ParamError]] = params
        self.source: Optional[Any] = source
        self.log_cb: Callable[[], None] = None

    def get_status(self) -> Status:
        return Status(self.code, self.messageParams, self.params)

    def set_source(self: GeneralError, source: Any) -> GeneralError:
        self.source = source
        return self

    def add_param_error(self, code: str, param: str, messageParams: Optional[List[str]]=None) -> GeneralError:
        if self.params is None:
            self.params = []
        self.params.append(ParamError(code, param, messageParams))
        return self

    def adds(self, params: List[ParamError]) -> GeneralError:
        if self.params is None:
            self.params = []
        if params is not None and len(params) > 0:
            self.params = self.params + params
        return self

    def set_log(self, log_cb: Callable[[], None]):
        self.log_cb = log_cb

def from_status(status: Status) -> GeneralError:
    return GeneralError(status.code, status.messageParams, status.params, None)
