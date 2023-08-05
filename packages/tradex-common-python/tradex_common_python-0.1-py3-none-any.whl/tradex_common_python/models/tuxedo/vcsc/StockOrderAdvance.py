from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderAdvanceReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderQuantity', 'orderPrice', \
                'bankCode', 'bankAccount', 'sellBuyType', 'orderType', 'phoneNumber', \
                'advanceOrderDate', 'securitiesType'

    def __init__(self):
        super(StockOrderAdvanceReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.bankCode: str = None
        self.bankAccount: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.phoneNumber: str = None
        self.advanceOrderDate: str = None
        self.securitiesType: str = None


class StockOrderAdvanceRes(Base):
    __slots__ = 'message', 'tempOrderNumber'

    def __init__(self):
        super(StockOrderAdvanceRes, self).__init__()
        self.message: str = None
        self.tempOrderNumber: str = None
