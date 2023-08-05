from tradex_common_python.models.tuxedo.vcsc.OrderTodayUnmatch import OrderTodayUnmatchReq

from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderModifyAllReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderPrice', 'newOrderPrice', \
                'orderType', 'sellBuyType', 'marketType', 'securitiesType', 'bankAccount'

    def __init__(self):
        super(StockOrderModifyAllReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderPrice: float = None
        self.newOrderPrice: float = None
        self.orderType: str = None
        self.sellBuyType: str = None
        self.marketType: str = None
        self.securitiesType: str = None
        self.bankAccount: str = None

    def to_order_today_unmatch_request(self):
        order_today_unmatch_req = OrderTodayUnmatchReq()
        order_today_unmatch_req.headers = self.headers
        order_today_unmatch_req.accountNumber = self.accountNumber
        order_today_unmatch_req.subNumber = self.subNumber
        order_today_unmatch_req.stockCode = self.stockCode
        return order_today_unmatch_req


class StockOrderModifyAllRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(StockOrderModifyAllRes, self).__init__()
        self.message: str = None
