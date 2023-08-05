from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class OrderTodayUnmatchReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'date', 'stockCode', \
                'lastBranchCode', 'lastOrderNumber', 'lastOrderPrice', 'fetchCount'

    def __init__(self):
        super(OrderTodayUnmatchReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.date: str = None
        self.stockCode: str = None
        self.lastBranchCode: str = None
        self.lastOrderNumber: str = None
        self.lastOrderPrice: str = None
        self.fetchCount: int = None


class OrderTodayUnmatchRes(Base):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderDate', 'orderTime', 'sellBuyType', \
                'orderType', 'orderQuantity', 'orderPrice', 'matchedQuantity', 'matchedPrice', 'matchedAmount', \
                'unmatchedQuantity', 'orderStatus', 'orderNumber', 'originalOrderNumber', 'username', 'branchCode', \
                'bankCode', 'bankName', 'channel', 'marketType'

    def __init__(self):
        super(OrderTodayUnmatchRes, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderDate: str = None
        self.orderTime: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.matchedQuantity: int = None
        self.matchedPrice: float = None
        self.matchedAmount: float = None
        self.unmatchedQuantity: int = None
        self.orderStatus: str = None
        self.orderNumber: str = None
        self.originalOrderNumber: str = None
        self.username: str = None
        self.branchCode: str = None
        self.bankCode: str = None
        self.bankName: str = None
        self.channel: str = None
        self.marketType: str = None
