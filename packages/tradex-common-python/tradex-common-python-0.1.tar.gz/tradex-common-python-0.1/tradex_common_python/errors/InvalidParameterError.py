from __future__ import annotations
from .GeneralError import GeneralError
from typing import Optional, List, Dict, Type
from ..models.Response import ParamError

class InvalidParameterError(GeneralError):
    def __init__(self, params: Optional[List[ParamError]]=None, source: Optional[Exception]= None) -> None:
        super(InvalidParameterError, self).__init__('INVALID_PARAMETER', None, params, source)
