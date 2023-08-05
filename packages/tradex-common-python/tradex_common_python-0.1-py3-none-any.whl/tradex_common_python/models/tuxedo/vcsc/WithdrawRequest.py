from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class WithdrawRequestReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'bankCode', 'amount', 'bankAccount', 'note'

    def __init__(self):
        super(WithdrawRequestReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.bankCode: str = None
        self.amount: float = None
        self.bankAccount: str = None
        self.note: str = None


class WithdrawRequestRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(WithdrawRequestRes, self).__init__()
        self.message: str = None
