from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountStockBalanceHistoryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'date', 'stockCode', 'lastStockCode', 'fetchCount'

    def __init__(self):
        super(AccountStockBalanceHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.lastStockCode: str = None
        self.date: str = None
        self.fetchCount: int = None


class AccountStockBalanceHistoryRes(Base):
    __slots__ = 'stockCode', 'balanceQuantity', 'date'

    def __init__(self):
        super(AccountStockBalanceHistoryRes, self).__init__()
        self.stockCode: str = None
        self.balanceQuantity: int = None
        self.date: str = None
