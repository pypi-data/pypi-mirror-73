from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountSellAbleReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'date', 'stockCode', 'fetchCount'

    def __init__(self):
        super(AccountSellAbleReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.date: str = None
        self.stockCode: str = None
        self.fetchCount: int = None


class AccountSellAbleRes(Base):
    __slots__ = 'stockCode', 'balanceQuantity', 'sellableQuantity', 'todayBuy', \
                'todaySell', 't1Buy', 't1Sell', 't2Buy', 't2Sell'

    def __init__(self):
        super(AccountSellAbleRes, self).__init__()
        self.stockCode: str = None
        self.balanceQuantity: int = None
        self.sellableQuantity: int = None
        self.todayBuy: int = None
        self.todaySell: int = None
        self.t1Buy: int = None
        self.t1Sell: int = None
        self.t2Buy: int = None
        self.t2Sell: int = None
