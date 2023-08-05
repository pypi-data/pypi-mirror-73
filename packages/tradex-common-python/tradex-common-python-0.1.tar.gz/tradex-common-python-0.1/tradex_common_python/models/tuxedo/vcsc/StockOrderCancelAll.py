from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from tradex_common_python.models.tuxedo.vcsc.OrderTodayUnmatch import OrderTodayUnmatchReq


class StockOrderCancelAllReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderPrice', 'orderType', 'sellBuyType'

    def __init__(self):
        super(StockOrderCancelAllReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderPrice: float = None  # if stockCode is None -> Ignore orderPrice
        self.orderType: str = None
        self.sellBuyType: str = None

    def to_order_today_unmatch_request(self):
        order_today_unmatch_req = OrderTodayUnmatchReq()
        order_today_unmatch_req.headers = self.headers
        order_today_unmatch_req.accountNumber = self.accountNumber
        order_today_unmatch_req.subNumber = self.subNumber
        order_today_unmatch_req.stockCode = self.stockCode
        return order_today_unmatch_req


class StockOrderCancelAllRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(StockOrderCancelAllRes, self).__init__()
        self.message: str = None
