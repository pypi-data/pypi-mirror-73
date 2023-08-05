from .InvalidParameterError import InvalidParameterError
from typing import Optional, List, Dict
from .codes import REQUIRED_FIELD

class FieldRequireError(InvalidParameterError):
    def __init__(self, field_name:str):
        super(FieldRequireError, self).__init__()
        self.add_param_error(REQUIRED_FIELD, field_name, [])