from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrStopOrderCancelAllReq(Request):
    __slots__ = 'accountNumber', 'futuresCode', 'stopPrice', 'sellBuyType'

    def __init__(self):
        super(DrStopOrderCancelAllReq, self).__init__()
        self.accountNumber: str = None
        self.futuresCode: str = None
        self.stopPrice: float = None  # if futuresCode is None -> Ignore orderPrice
        self.sellBuyType: str = None


class DrOrderCancelAllRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(DrOrderCancelAllRes, self).__init__()
        self.message: str = None
