from typing import List, Optional, Type, Dict
from .Base import Base

class ParamError(Base):
    __slots__ = 'code', 'param', 'messageParams'
    def __init__(self, code: str, param: str, messageParams: Optional[List[str]]=None):
        self.code: str = code
        self.param: str = param
        self.messageParams: List[str] = messageParams

    def to_dict(self):
        return {
            'code': self.code,
            'param': self.param,
            'messageParams': self.messageParams,
        }


class Status(Base):
    __slots__ = 'code', 'params', 'messageParams'
    def __init__(self, code: str, messageParams: Optional[List[str]]=None, params: Optional[List[ParamError]]=None):
        self.code = code
        self.messageParams = messageParams
        self.params = params

    def add_param(self, code: str, param: str, messageParams: Optional[List[str]]=None):
        if self.params is None:
            self.params: Optional[List[ParamError]] = []
        self.params.append(ParamError(code, param, messageParams))
        return self

    def to_dict(self):
        params = []
        for param in ([] if self.params is None else self.params):
            params.append(param.to_dict())

        return {
            'code': self.code,
            'params': params,
            'messageParams': self.messageParams,
        }
        

class Response(Base):
    __slots__ = 'data', 'status'

    def __init__(self, data, status: Status):
        self.data = data
        self.status: Status = status

    # def to_dict(self):
    #     data: Dict = {}
    #     if self.data is not None:
    #         if hasattr(self.data, 'to_dict'):
    #             data['data'] = self.data.to_dict()
    #         else:
    #             data['data'] = self.data
    #     if self.status is not None:
    #         data['status'] = self.status.to_dict()
    #     return data
