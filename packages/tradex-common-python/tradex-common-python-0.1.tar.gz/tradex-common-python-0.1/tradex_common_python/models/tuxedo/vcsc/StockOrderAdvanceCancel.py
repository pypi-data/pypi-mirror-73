from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderAdvanceCancelReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'advanceOrderDate', 'orderNumber'

    def __init__(self):
        super(StockOrderAdvanceCancelReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.advanceOrderDate: str = None
        self.orderNumber: str = None


class StockOrderAdvanceCancelRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(StockOrderAdvanceCancelRes, self).__init__()
        self.message: str = None
