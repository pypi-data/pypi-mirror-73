from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderOddlotReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderQuantity', 'orderPrice', \
                'securitiesType', 'bankCode', 'bankAccount'

    def __init__(self):
        super(StockOrderOddlotReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.securitiesType: str = None
        self.bankCode: str = None
        self.bankAccount: str = None


class StockOrderOddlotRes(Base):
    __slots__ = 'message', 'orderNumber'

    def __init__(self):
        super(StockOrderOddlotRes, self).__init__()
        self.message: str = None
        self.orderNumber: str = None
