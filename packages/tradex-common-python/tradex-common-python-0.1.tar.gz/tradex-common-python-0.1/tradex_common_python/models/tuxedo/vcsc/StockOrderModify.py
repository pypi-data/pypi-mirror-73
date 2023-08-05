import enum
from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderModifyReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderQuantity', 'orderPrice', \
                'orderNumber', 'marketType', 'branchCode', 'bankCode', 'sellBuyType', 'orderType', \
                'securitiesType', 'bankAccount', 'bankName'

    def __init__(self):
        super(StockOrderModifyReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.orderNumber: str = None
        self.marketType: str = None
        self.branchCode: str = None
        self.bankCode: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.securitiesType: str = None
        self.bankAccount: str = None
        self.bankName: str = None


class StockOrderModifyRes(Base):
    __slots__ = 'orderNumber', 'type'

    def __init__(self):
        super(StockOrderModifyRes, self).__init__()
        self.orderNumber: str = None
        self.type: str = None


class SuccessType(enum.Enum):
    FULL = 'FULL'
    PARTIAL = 'PARTIAL'
