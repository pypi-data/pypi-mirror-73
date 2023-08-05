from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderOddlotUnmatchReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'lastBranchCode', 'lastOrderNumber', 'fetchCount'

    def __init__(self):
        super(StockOrderOddlotUnmatchReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.lastBranchCode: str = None
        self.lastOrderNumber: str = None
        self.fetchCount: int = None


class StockOrderOddlotUnmatchRes(Base):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderNumber', 'sellBuyType', 'orderQuantity', \
                'orderPrice', 'branchCode', 'status', 'bankName',

    def __init__(self):
        super(StockOrderOddlotUnmatchRes, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderNumber: str = None
        self.sellBuyType: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.branchCode: str = None
        self.status: str = None
        self.bankName: str = None
