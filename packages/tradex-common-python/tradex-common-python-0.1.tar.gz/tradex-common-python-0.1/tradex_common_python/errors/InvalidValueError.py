from .InvalidParameterError import InvalidParameterError
from typing import Optional, List, Dict
from .codes import INVALID_VALUE

class InvalidValueError(InvalidParameterError):
    def __init__(self, param_name:str, message_params:Optional[List[str]]=None):
        super(InvalidValueError, self).__init__()
        self.add_param_error(INVALID_VALUE, param_name, message_params)