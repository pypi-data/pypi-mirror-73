from .InvalidParameterError import InvalidParameterError
from .codes import LENGTH_INVALID


class FieldLengthError(InvalidParameterError):
    def __init__(self, field_name: str, length: int):
        super(FieldLengthError, self).__init__()
        self.add_param_error(LENGTH_INVALID, field_name, ['length must be = ' + str(length)])
