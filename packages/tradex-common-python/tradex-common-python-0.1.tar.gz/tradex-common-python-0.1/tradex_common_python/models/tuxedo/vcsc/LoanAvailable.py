from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class LoanAvailableReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'loanBankCode', 'lastSettleBankCode', 'lastMatchDate', \
                'lastSettleDate', 'lastLoanOrderType', 'fetchCount'

    def __init__(self):
        super(LoanAvailableReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.loanBankCode: str = None
        self.lastSettleBankCode: int = None
        self.lastMatchDate: str = None
        self.lastSettleDate: str = None
        self.lastLoanOrderType: str = None
        self.fetchCount: int = None


class LoanAvailableRes(Base):
    __slots__ = 'matchDate', 'settleDate', 'matchAmount', 'tradingFee', 'tax', 'adjustAmount', \
                'loanPeriod', 'feeRate', 'estimatedFee', 'possibleAmount', 'settleBankCode', \
                'loanBankName', 'loanOrderType', 'loanOrderName'

    def __init__(self):
        super(LoanAvailableRes, self).__init__()
        self.matchDate: str = None
        self.settleDate: str = None
        self.matchAmount: float = None
        self.tradingFee: float = None
        self.adjustAmount: float = None
        self.loanPeriod: int = None
        self.feeRate: float = None
        self.estimatedFee: float = None
        self.possibleAmount: float = None
        self.tax: float = None
        self.settleBankCode: str = None
        self.loanBankName: str = None
        self.loanOrderType: str = None
        self.loanOrderName: str = None
