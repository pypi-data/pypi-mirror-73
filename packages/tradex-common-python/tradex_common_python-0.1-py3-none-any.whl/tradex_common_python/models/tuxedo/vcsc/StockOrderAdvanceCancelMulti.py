from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from typing import List


class StockOrderAdvanceCancelMultiReq(Request):
    __slots__ = 'orderList'

    def __init__(self):
        super(StockOrderAdvanceCancelMultiReq, self).__init__()
        self.orderList: List[AdvanceOrderCancelItem] = []


class AdvanceOrderCancelItem(Base):
    __slots__ = 'accountNumber', 'subNumber', 'orderNumber', 'advanceOrderDate'

    def __init__(self):
        super(AdvanceOrderCancelItem, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.orderNumber: str = None
        self.advanceOrderDate: str = None


class StockOrderAdvanceCancelMultiRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(StockOrderAdvanceCancelMultiRes, self).__init__()
        self.message: str = None
