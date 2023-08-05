from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrImWithdrawRequestReq(Request):
    __slots__ = 'accountNumber', 'amount', 'note', 'sourceBank', 'destBank', 'feeAmount', 'adjustedAmount', \
                'receivedAmount', 'feeType'

    def __init__(self):
        super(DrImWithdrawRequestReq, self).__init__()
        self.accountNumber: str = None
        self.amount: float = None
        self.note: str = None
        self.sourceBank: str = None
        self.destBank: str = None
        self.feeAmount: float = None
        self.adjustedAmount: float = None
        self.receivedAmount: float = None
        self.feeType: str = None


class DrImWithdrawRequestRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(DrImWithdrawRequestRes, self).__init__()
        self.message: str = None
