from tradex_common_python.models.tuxedo.vcsc.StockOrderModify import StockOrderModifyReq

from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderCancelReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'orderNumber', 'branchCode'

    def __init__(self):
        super(StockOrderCancelReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.orderNumber: str = None
        self.branchCode: str = None

    @classmethod
    def from_request(cls, request: StockOrderModifyReq):
        instance = cls()
        instance.headers = request.headers
        instance.sourceIp = request.sourceIp
        instance.deviceType = request.deviceType
        instance.accountNumber = request.accountNumber
        instance.subNumber = request.subNumber
        instance.orderNumber = request.orderNumber
        instance.branchCode = request.branchCode
        return instance


class StockOrderCancelRes(Base):
    __slots__ = 'orderNumber'

    def __init__(self):
        super(StockOrderCancelRes, self).__init__()
        self.orderNumber: str = None
