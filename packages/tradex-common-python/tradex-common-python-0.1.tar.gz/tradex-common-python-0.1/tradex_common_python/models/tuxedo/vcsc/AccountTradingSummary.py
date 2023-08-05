from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountTradingSummaryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'fromDate', 'toDate', 'sellBuyType', 'marketType', \
                'stockCode', 'lastMatchDate', 'fetchCount', 'lastSellBuyType', 'lastStockCode'

    def __init__(self):
        super(AccountTradingSummaryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.sellBuyType: str = None
        self.marketType: str = None
        self.stockCode: str = None
        self.lastMatchDate: str = None
        self.lastSellBuyType: str = None
        self.lastStockCode: str = None
        self.fetchCount: int = None


class AccountTradingSummaryRes(Base):
    __slots__ = 'stockCode', 'sellBuyType', 'averagePrice', 'orderQuantity', 'amount', 'fee', \
                'tax', 'adjustedAmount', 'matchDate', 'unmatchQuantity', 'orderPrice', 'matchQuantity'

    def __init__(self):
        super(AccountTradingSummaryRes, self).__init__()
        self.stockCode: str = None
        self.sellBuyType: str = None
        self.averagePrice: float = None
        self.orderQuantity: int = None
        self.amount: float = None
        self.fee: float = None
        self.tax: float = None
        self.adjustedAmount: float = None
        self.matchDate: str = None
        self.unmatchQuantity: int = None
        self.orderPrice: float = None
        self.matchQuantity: int = None
