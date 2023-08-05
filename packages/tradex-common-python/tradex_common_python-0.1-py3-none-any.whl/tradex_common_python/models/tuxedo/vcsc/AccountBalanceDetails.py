from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountBalanceDetailsReq(Request):
    __slots__ = 'date', 'stockCode', 'accountNumber', 'subNumber', 'lastStockCode', 'fetchCount'

    def __init__(self):
        super(AccountBalanceDetailsReq, self).__init__()
        self.date: str = None
        self.stockCode: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.lastStockCode: str = None
        self.fetchCount: int = None


class AccountBalanceDetailsRes(Base):
    __slots__ = 'stockCode', 'totalBalance', 'availableQuantity', 'mortgageQuantity', \
                'blockadeQuantity', 'tBuyQuantity', 't1BuyQuantity', \
                't2BuyQuantity', 't3BuyQuantity', 'tSellQuantity', \
                't1SellQuantity', 't2SellQuantity', 't3SellQuantity', \
                'unmatchedSellT', 'avgBuyingPrice', 'marketPrice', \
                'totalBuyingAmount', 'totalMarketValue', 'profitOnLoss', \
                'profitOnLossRate', 'marginRatio', 'bonusShares', \
                'subscriptionsQuantity', 'registeredSubscriptionsQuantity', 'cashDividends'

    def __init__(self):
        super(AccountBalanceDetailsRes, self).__init__()
        self.stockCode: str = None
        self.totalBalance: int = None
        self.availableQuantity: int = None
        self.mortgageQuantity: int = None
        self.blockadeQuantity: int = None
        self.tBuyQuantity: int = None
        self.t1BuyQuantity: int = None
        self.t2BuyQuantity: int = None
        self.t3BuyQuantity: int = None
        self.tSellQuantity: int = None
        self.t1SellQuantity: int = None
        self.t2SellQuantity: int = None
        self.t3SellQuantity: int = None
        self.unmatchedSellT: float = None
        self.avgBuyingPrice: float = None
        self.marketPrice: float = None
        self.totalBuyingAmount: int = None
        self.totalMarketValue: int = None
        self.profitOnLoss: float = None
        self.profitOnLossRate: float = None
        self.marginRatio: float = None
        self.bonusShares: int = None
        self.subscriptionsQuantity: int = None
        self.registeredSubscriptionsQuantity: int = None
        self.cashDividends: float = None
