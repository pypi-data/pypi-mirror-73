from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class TransferStockBalanceReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'lastStockCode', 'fetchCount'

    def __init__(self):
        super(TransferStockBalanceReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.lastStockCode: str = None
        self.fetchCount: int = None


class TransferStockBalanceRes(Base):
    __slots__ = 'stockCode', 'stockName', 'availableQuantity', 'limitAvailableQuantity'

    def __init__(self):
        super(TransferStockBalanceRes, self).__init__()
        self.stockCode: str = None
        self.stockName: str = None
        self.availableQuantity: int = None
        self.limitAvailableQuantity: int = None
