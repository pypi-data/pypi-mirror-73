from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class MarginReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'symbolCode'

    def __init__(self):
        super(MarginReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.symbolCode: str = None


class MarginRes(Base):
    __slots__ = 'ratio'

    def __init__(self):
        super(MarginRes, self).__init__()
        self.ratio: float = None
