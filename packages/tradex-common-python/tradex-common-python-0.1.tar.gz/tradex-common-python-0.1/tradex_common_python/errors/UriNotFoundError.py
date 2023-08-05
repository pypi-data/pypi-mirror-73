from .GeneralError import GeneralError

class UriNotFoundError(GeneralError):
    def __init__(self):
        super(UriNotFoundError, self).__init__('URI_NOT_FOUND')
