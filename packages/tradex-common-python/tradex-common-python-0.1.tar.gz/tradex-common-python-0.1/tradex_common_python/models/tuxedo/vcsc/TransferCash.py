from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class TransferCashReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'receivedAccountNumber', 'receivedSubNumber', 'amount', 'note'

    def __init__(self):
        super(TransferCashReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.receivedAccountNumber: str = None
        self.receivedSubNumber: str = None
        self.amount: float = None
        self.note: str = None


class TransferCashRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(TransferCashRes, self).__init__()
        self.message: str = None
