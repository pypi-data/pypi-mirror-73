from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrCashWithdrawRequestReq(Request):
    __slots__ = 'accountNumber', 'amount', 'note', 'bankAccount', 'bankCode'

    def __init__(self):
        super(DrCashWithdrawRequestReq, self).__init__()
        self.accountNumber: str = None
        self.amount: float = None
        self.note: str = None
        self.bankAccount: str = None
        self.bankCode: str = None


class DrCashWithdrawRequestRes(Base):
    __slots__ = 'transactionDate', 'sequenceNumber', 'previousCashBalance', 'cashBalance', 'fee', 'receivedCash'

    def __init__(self):
        super(DrCashWithdrawRequestRes, self).__init__()
        self.transactionDate: str = None
        self.sequenceNumber: str = None
        self.previousCashBalance: float = None
        self.cashBalance: float = None
        self.fee: float = None
        self.receivedCash: float = None
