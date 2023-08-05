from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountTransactionHistoryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'fromDate', 'toDate', 'tradingType', 'lastTradingDate', \
                'lastTradingSequence', 'fetchCount'

    def __init__(self):
        super(AccountTransactionHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.tradingType: str = None
        self.lastTradingDate: str = None
        self.lastTradingSequence: str = None
        self.fetchCount: int = None


class AccountTransactionHistoryRes(Base):
    __slots__ = 'accountNumber', 'subNumber', 'tradingDate', 'transactionName', 'stockCode', \
                'balanceQuantity', 'tradingQuantity', 'tradingPrice', 'tradingAmount', 'fee', 'loanInterest', \
                'adjustedAmount', 'tradingSequence', 'prevDepositAmount', 'depositAmount', 'channel', 'remarks'

    def __init__(self):
        super(AccountTransactionHistoryRes, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.tradingDate: str = None
        self.transactionName: str = None
        self.stockCode: str = None
        self.balanceQuantity: int = None
        self.tradingQuantity: int = None
        self.tradingPrice: float = None
        self.tradingAmount: float = None
        self.fee: float = None
        self.loanInterest: float = None
        self.adjustedAmount: float = None
        self.tradingSequence: str = None
        self.prevDepositAmount: float = None
        self.depositAmount: float = None
        self.channel: str = None
        self.remarks: str = None
