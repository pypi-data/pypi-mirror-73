from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderAdvPlaceReq(Request):
    __slots__ = 'accountNumber', 'code', 'orderQuantity', 'orderPrice', 'sellBuyType',  'orderType', \
                'advanceOrderType', 'marketSession', 'fromDate', 'toDate'

    def __init__(self):
        super(DrOrderAdvPlaceReq, self).__init__()
        self.accountNumber: str = None
        self.code: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.advanceOrderType: str = None
        self.marketSession: str = None
        self.fromDate: str = None
        self.toDate: str = None


class DrOrderAdvPlaceRes(Base):
    __slots__ = 'orderNumber'

    def __init__(self):
        super(DrOrderAdvPlaceRes, self).__init__()
        self.orderNumber: str = None
