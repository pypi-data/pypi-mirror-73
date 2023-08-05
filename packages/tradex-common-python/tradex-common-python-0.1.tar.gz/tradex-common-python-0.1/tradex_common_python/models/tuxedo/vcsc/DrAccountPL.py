from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from typing import List


class DrAccountPLReq(Request):
    __slots__ = 'accountNumber', 'fromDate', 'toDate', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrAccountPLReq, self).__init__()
        self.accountNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.lastNextKey: str = None
        self.fetchCount: int = None


class DrAccountPLRes(Base):
    __slots__ = 'closedLongQuantity', 'closedShortQuantity', 'realizedPL', 'fee', 'tax', 'netProfitLoss', \
                'longQuantity', 'shortQuantity', 'unrealizedPL', 'profitLossItems'

    def __init__(self):
        super(DrAccountPLRes, self).__init__()
        self.closedLongQuantity: int = None
        self.closedShortQuantity: int = None
        self.realizedPL: float = None
        self.fee: float = None
        self.tax: float = None
        self.netProfitLoss: float = None
        self.longQuantity: int = None
        self.shortQuantity: int = None
        self.unrealizedPL: float = None
        self.profitLossItems: List[ProfitLossItem] = None


class ProfitLossItem(Base):
    __slots__ = 'code', 'lastPrice', 'closedLongQuantity', 'closedShortQuantity', 'realizedPL', 'fee', 'tax', \
                'netProfitLoss', 'longQuantity', 'shortQuantity', 'unrealizedPL', 'nextKey'

    def __init__(self):
        super(ProfitLossItem, self).__init__()
        self.code: str = None
        self.lastPrice: float = None
        self.closedLongQuantity: int = None
        self.closedShortQuantity: int = None
        self.realizedPL: float = None
        self.fee: float = None
        self.tax: float = None
        self.netProfitLoss: float = None
        self.longQuantity: int = None
        self.shortQuantity: int = None
        self.unrealizedPL: float = None
        self.nextKey: str = None

