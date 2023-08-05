from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockHolderRegisterReq(Request):
    __slots__ = 'accountNumber', 'type', 'stockCode'

    def __init__(self):
        super(StockHolderRegisterReq, self).__init__()
        self.accountNumber: str = None
        self.type: str = None
        self.stockCode: str = None


class StockHolderRegisterRes(Base):
    __slots__ = 'status'

    def __init__(self):
        super(StockHolderRegisterRes, self).__init__()
        self.status: str = None
