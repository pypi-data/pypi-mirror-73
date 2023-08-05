from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrHistorySettlementReq(Request):
    __slots__ = 'fromDate', 'toDate', 'accountNumber', 'subNumber', 'lastTradingDate', 'lastSettleDate', 'fetchCount'

    def __init__(self):
        super(DrHistorySettlementReq, self).__init__()
        self.fromDate: str = None
        self.toDate: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.lastTradingDate: str = None
        self.lastSettleDate: str = None
        self.fetchCount: int = None


class DrHistorySettlementRes(Base):
    __slots__ = 'tradingDate', 'settleDate', 'variationMargin', 'fee', 'tax', 'depositBalance', \
                'deficitAmount', 'variationMarginStatus', 'feeStatus', 'taxStatus', 'totalFee'

    def __init__(self):
        super(DrHistorySettlementRes, self).__init__()
        self.tradingDate: str = None
        self.settleDate: str = None
        self.variationMargin: float = None
        self.fee: float = None
        self.tax: float = None
        self.depositBalance: float = None
        self.deficitAmount: float = None
        self.variationMarginStatus: bool = None
        self.feeStatus: bool = None
        self.taxStatus: bool = None
        self.totalFee: float = None
