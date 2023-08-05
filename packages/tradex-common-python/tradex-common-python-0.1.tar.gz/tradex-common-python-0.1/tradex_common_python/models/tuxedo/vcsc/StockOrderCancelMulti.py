from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from typing import List


class StockOrderCancelMultiReq(Request):
    __slots__ = 'orderList'

    def __init__(self):
        super(StockOrderCancelMultiReq, self).__init__()
        self.orderList: List[OrderCancelItem] = []


class OrderCancelItem(Base):
    __slots__ = 'accountNumber', 'subNumber', 'orderNumber', 'branchCode'

    def __init__(self):
        super(OrderCancelItem, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.orderNumber: str = None
        self.branchCode: str = None


class StockOrderCancelMultiRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(StockOrderCancelMultiRes, self).__init__()
        self.message: str = None
