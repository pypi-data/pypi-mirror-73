from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class RightCancelReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'baseDate', 'quantity', 'amount', 'tradeNumber', \
                'sequenceNumber', 'bankCode', 'bankAccount', 'rightType'

    def __init__(self):
        super(RightCancelReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.baseDate: str = None
        self.quantity: int = None
        self.amount: float = None
        self.tradeNumber: str = None
        self.sequenceNumber: int = None
        self.bankCode: str = None
        self.bankAccount: str = None
        self.rightType: str = None


class RightCancelRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(RightCancelRes, self).__init__()
        self.message: str = None
