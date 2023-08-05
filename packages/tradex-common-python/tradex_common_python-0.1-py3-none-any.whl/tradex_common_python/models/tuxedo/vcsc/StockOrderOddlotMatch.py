from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderOddlotMatchReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'matchType', 'lastBranchCode', 'lastOrderNumber', 'fetchCount'

    def __init__(self):
        super(StockOrderOddlotMatchReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.matchType: str = None
        self.lastBranchCode: str = None
        self.lastOrderNumber: str = None
        self.fetchCount: int = None


class StockOrderOddlotMatchRes(Base):
    __slots__ = 'branchCode', 'orderNumber', 'accountNumber', 'subNumber', 'accountName', 'stockCode', 'sellBuyType', \
                'modifyCancelType', 'orderQuantity', 'unmatchedQuantity', 'matchedQuantity', 'matchedPrice', 'matchType', \
                'orderPrice', 'orderDate', 'cancelReason'

    def __init__(self):
        super(StockOrderOddlotMatchRes, self).__init__()
        self.branchCode: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.orderNumber: str = None
        self.accountName: str = None
        self.stockCode: str = None
        self.sellBuyType: str = None
        self.modifyCancelType: str = None
        self.orderQuantity: int = None
        self.unmatchedQuantity: int = None
        self.matchedQuantity: int = None
        self.matchedPrice: float = None
        self.orderPrice: float = None
        self.matchType: str = None
        self.orderDate: str = None
        self.cancelReason: str = None
