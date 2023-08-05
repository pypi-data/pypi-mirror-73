from tradex_common_python.models.Request import Request


class CertLoginReq(Request):
    __slots__ = 'username', 'thumbprint'

    def __init__(self):
        super(CertLoginReq, self).__init__()
        self.username: str = None
        self.thumbprint: str = None
