from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrStopOrderModifyAllReq(Request):
    __slots__ = 'accountNumber', 'futuresCode', 'stopPrice', 'newStopPrice', 'sellBuyType'

    def __init__(self):
        super(DrStopOrderModifyAllReq, self).__init__()
        self.accountNumber: str = None
        self.futuresCode: str = None
        self.stopPrice: float = None
        self.newStopPrice: float = None
        self.sellBuyType: str = None


class DrOrderModifyAllRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(DrOrderModifyAllRes, self).__init__()
        self.message: str = None
