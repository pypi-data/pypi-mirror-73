from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderOddlotCancelReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'orderNumber', 'rejectNote', 'branchCode'

    def __init__(self):
        super(StockOrderOddlotCancelReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.orderNumber: str = None
        self.branchCode: str = None
        self.rejectNote: str = None


class StockOrderOddlotCancelRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(StockOrderOddlotCancelRes, self).__init__()
        self.message: str = None
