from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class CertUnRegisterReq(Request):
    __slots__ = 'username', 'thumbprint'

    def __init__(self):
        super(CertUnRegisterReq, self).__init__()
        self.username: str = None
        self.thumbprint: str = None


class CertUnRegisterRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(CertUnRegisterRes, self).__init__()
        self.message: str = None
