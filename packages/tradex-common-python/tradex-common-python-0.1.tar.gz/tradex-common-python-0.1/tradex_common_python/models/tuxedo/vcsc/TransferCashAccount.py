from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class TransferCashAccountReq(Request):
    __slots__ = 'accountNumber', 'subNumber'

    def __init__(self):
        super(TransferCashAccountReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None


class TransferCashAccountRes(Base):
    __slots__ = 'accountNumber', 'subNumber', 'accountName'

    def __init__(self):
        super(TransferCashAccountRes, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.accountName: str = None
