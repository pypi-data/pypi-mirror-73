from tradex_common_python.models.tuxedo.vcsc.StockOrderModify import StockOrderModifyReq

from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'orderQuantity', 'orderPrice', \
                'bankCode', 'sellBuyType', 'orderType', 'securitiesType', 'bankAccount', 'bankName'

    def __init__(self):
        super(StockOrderReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.bankCode: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.securitiesType: str = None
        self.bankAccount: str = None
        self.bankName: str = None

    @classmethod
    def from_request(cls, request: StockOrderModifyReq):
        instance = cls()
        instance.headers = request.headers
        instance.sourceIp = request.sourceIp
        instance.deviceType = request.deviceType
        instance.accountNumber = request.accountNumber
        instance.subNumber = request.subNumber
        instance.stockCode = request.stockCode
        instance.orderQuantity = request.orderQuantity
        instance.orderPrice = request.orderPrice
        instance.bankCode = request.bankCode
        instance.sellBuyType = request.sellBuyType
        instance.orderType = request.orderType
        instance.securitiesType = request.securitiesType
        instance.bankAccount = request.bankAccount
        return instance


class StockOrderRes(Base):
    __slots__ = 'message', 'orderNumber'

    def __init__(self):
        super(StockOrderRes, self).__init__()
        self.message: str = None
        self.orderNumber: str = None
