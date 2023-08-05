from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from typing import List


class DrAccountPLCumulativeReq(Request):
    __slots__ = 'accountNumber', 'fromDate', 'toDate', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrAccountPLCumulativeReq, self).__init__()
        self.accountNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.lastNextKey: str = None
        self.fetchCount: int = None


class DrAccountPLCumulativeRes(Base):
    __slots__ = 'realizedPL', 'unrealizedPL', 'fee', 'tax', 'netProfitLoss', 'profitLossItems'

    def __init__(self):
        super(DrAccountPLCumulativeRes, self).__init__()
        self.realizedPL: float = None
        self.unrealizedPL: float = None
        self.fee: float = None
        self.tax: float = None
        self.netProfitLoss: float = None
        self.profitLossItems: List[ProfitLossItemCumulative] = None


class ProfitLossItemCumulative(Base):
    __slots__ = 'code', 'date', 'realizedPL', 'unrealizedPL', 'fee', 'tax', 'netProfitLoss', 'nextKey'

    def __init__(self):
        super(ProfitLossItemCumulative, self).__init__()
        self.code: str = None
        self.date: str = None
        self.realizedPL: float = None
        self.unrealizedPL: float = None
        self.fee: float = None
        self.tax: float = None
        self.netProfitLoss: float = None
        self.nextKey: str = None

