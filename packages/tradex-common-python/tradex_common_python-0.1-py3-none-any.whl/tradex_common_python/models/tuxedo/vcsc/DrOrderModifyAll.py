from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderModifyAllReq(Request):
    __slots__ = 'accountNumber', 'futuresCode', 'orderPrice', 'newOrderPrice', 'orderType', 'sellBuyType'

    def __init__(self):
        super(DrOrderModifyAllReq, self).__init__()
        self.accountNumber: str = None
        self.futuresCode: str = None
        self.orderPrice: float = None
        self.newOrderPrice: float = None
        self.orderType: str = None
        self.sellBuyType: str = None


class DrOrderModifyAllRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(DrOrderModifyAllRes, self).__init__()
        self.message: str = None
