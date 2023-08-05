from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class StockOrderOddlotSellableReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'lastStockCode', 'fetchCount'

    def __init__(self):
        super(StockOrderOddlotSellableReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.lastStockCode: str = None
        self.fetchCount: int = None


class StockOrderOddlotSellableRes(Base):
    __slots__ = 'accountNumber', 'subNumber', 'stockCode', 'balanceQuantity', 'sellableQuantity', \
                't3Sell', 't3Buy', 't2Sell', 't2Buy', 't1Sell', 't1Buy', 'todaySell', 'todayBuy', 'todayOrder'

    def __init__(self):
        super(StockOrderOddlotSellableRes, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.stockCode: str = None
        self.balanceQuantity: int = None
        self.sellableQuantity: int = None
        self.t3Sell: int = None
        self.t3Buy: int = None
        self.t2Sell: int = None
        self.t2Buy: int = None
        self.t1Sell: int = None
        self.t1Buy: int = None
        self.todaySell: int = None
        self.todayBuy: int = None
        self.todayOrder: int = None
