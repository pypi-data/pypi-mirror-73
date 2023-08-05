from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class CertUpdateReq(Request):
    __slots__ = 'username', 'thumbprint'

    def __init__(self):
        super(CertUpdateReq, self).__init__()
        self.username: str = None
        self.thumbprint: str = None


class CertUpdateRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(CertUpdateRes, self).__init__()
        self.message: str = None
