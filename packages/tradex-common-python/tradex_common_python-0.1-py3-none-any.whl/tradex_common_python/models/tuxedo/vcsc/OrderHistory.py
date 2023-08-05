from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class OrderHistoryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'fromDate', 'toDate', 'stockCode', 'sellBuyType', 'matchType', \
                'sortType', 'lastOrderDate', 'lastBranchCode', 'lastOrderNumber', 'lastMatchPrice', 'fetchCount', \
                'marketType'

    def __init__(self):
        super(OrderHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.stockCode: str = None
        self.sellBuyType: str = None
        self.matchType: str = None
        self.sortType: str = None
        self.lastOrderDate: str = None
        self.lastBranchCode: str = None
        self.lastOrderNumber: str = None
        self.lastMatchPrice: float = None
        self.fetchCount: int = None
        self.marketType: str = None


class OrderHistoryRes(Base):
    __slots__ = 'accountNumber', 'stockCode', 'orderDate', 'orderTime', 'sellBuyType', 'orderType', 'orderQuantity', \
                'orderPrice', 'orderAmount', 'matchedQuantity', 'matchedPrice', 'matchedAmount', 'unmatchedQuantity', \
                'modifyCancelType', 'modifyCancelQuantity', 'orderStatus', 'orderNumber', 'originalOrderNumber', \
                'username', 'branchCode', 'subNumber', 'bankName'

    def __init__(self):
        super(OrderHistoryRes, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderDate: str = None
        self.orderTime: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.orderAmount: float = None
        self.matchedQuantity: int = None
        self.matchedPrice: float = None
        self.matchedAmount: float = None
        self.unmatchedQuantity: int = None
        self.modifyCancelType: str = None
        self.modifyCancelQuantity: int = None
        self.orderStatus: str = None
        self.orderNumber: str = None
        self.originalOrderNumber: str = None
        self.username: str = None
        self.branchCode: str = None
        self.bankName: str = None
