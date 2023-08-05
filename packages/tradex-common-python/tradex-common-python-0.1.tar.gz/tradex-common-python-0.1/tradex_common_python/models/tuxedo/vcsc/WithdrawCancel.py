from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class WithdrawCancelReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'transactionType', 'transactionCode', 'sequenceNumber', \
                'amount', 'bankCode', 'bankAccount', 'note'

    def __init__(self):
        super(WithdrawCancelReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.transactionType: str = None
        self.transactionCode: str = None
        self.sequenceNumber: str = None
        self.amount: float = None
        self.bankCode: str = None
        self.bankAccount: str = None
        self.note: str = None


class WithdrawCancelRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(WithdrawCancelRes, self).__init__()
        self.message: str = None
