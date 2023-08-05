from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderAdvanceHistoryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'marketType', \
                'sellBuyType', 'lastOrderDate', 'lastOrderNumber', 'fetchCount'

    def __init__(self):
        super(StockOrderAdvanceHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.marketType: str = None
        self.sellBuyType: str = None
        self.lastOrderDate: str = None
        self.lastOrderNumber: str = None
        self.fetchCount: int = None


class StockOrderAdvanceHistoryRes(Base):
    __slots__ = 'accountNumber', 'subNumber', 'orderDate', 'orderTime', 'orderNumber', 'stockCode', 'sellBuyType', \
                'orderType', 'orderQuantity', 'orderPrice', 'orderStatus', 'username', 'channel', 'branchCode', \
                'phoneNumber'

    def __init__(self):
        super(StockOrderAdvanceHistoryRes, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.orderDate: str = None
        self.orderTime: str = None
        self.orderNumber: str = None
        self.stockCode: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.orderStatus: str = None
        self.username: str = None
        self.channel: str = None
        self.branchCode: str = None
        self.phoneNumber: str = None
