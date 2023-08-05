from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class CertRegisterReq(Request):
    __slots__ = 'username', 'thumbprint'

    def __init__(self):
        super(CertRegisterReq, self).__init__()
        self.username: str = None
        self.thumbprint: str = None


class CertRegisterRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(CertRegisterRes, self).__init__()
        self.message: str = None
