from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrImFeeReq(Request):
    __slots__ = 'accountNumber', 'sendingBank', 'receivingBank', 'amount', 'type'

    def __init__(self):
        super(DrImFeeReq, self).__init__()
        self.accountNumber: str = None
        self.sendingBank: str = None
        self.receivingBank: str = None
        self.amount: float = None
        self.type: str = None


class DrImFeeRes(Base):
    __slots__ = 'feeAmount', 'adjustedAmount', 'receivedAmount', 'feeType'

    def __init__(self):
        super(DrImFeeRes, self).__init__()
        self.feeAmount: float = None
        self.adjustedAmount: float = None
        self.receivedAmount: float = None
        self.feeType: str = None
