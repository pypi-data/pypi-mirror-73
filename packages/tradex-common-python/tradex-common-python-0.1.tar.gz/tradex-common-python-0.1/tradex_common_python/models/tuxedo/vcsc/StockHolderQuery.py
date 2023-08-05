from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockHolderQueryReq(Request):
    __slots__ = 'accountNumber', 'stockCode'

    def __init__(self):
        super(StockHolderQueryReq, self).__init__()
        self.accountNumber: str = None
        self.stockCode: str = None


class StockHolderQueryRes(Base):
    __slots__ = 'status'

    def __init__(self):
        super(StockHolderQueryRes, self).__init__()
        self.status: str = None
