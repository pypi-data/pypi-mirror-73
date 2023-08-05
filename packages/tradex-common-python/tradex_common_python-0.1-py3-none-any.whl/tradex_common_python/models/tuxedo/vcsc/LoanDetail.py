from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class LoanDetailReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'loanBankCode', 'settleBankCode', 'matchDate', \
                'settleDate', 'loanOrderType', 'lastSettleBankCode', 'lastStockCode', 'lastLoanOrderType'

    def __init__(self):
        super(LoanDetailReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.loanBankCode: str = None
        self.settleBankCode: str = None
        self.matchDate: str = None
        self.settleDate: str = None
        self.loanOrderType: str = None
        self.lastSettleBankCode: str = None
        self.lastStockCode: str = None
        self.lastLoanOrderType: str = None


class LoanDetailRes(Base):
    __slots__ = 'matchDate', 'settleDate', 'stockCode', 'matchQuantity', 'matchAmount', 'tradingFee', \
                'adjustAmount', 'possibleAmount', 'tax', 'settleBankCode', 'settleBankName', 'loanOrderType'

    def __init__(self):
        super(LoanDetailRes, self).__init__()
        self.matchDate: str = None
        self.settleDate: str = None
        self.stockCode: str = None
        self.matchQuantity: int = None
        self.matchAmount: float = None
        self.tradingFee: float = None
        self.adjustAmount: float = None
        self.possibleAmount: float = None
        self.tax: float = None
        self.settleBankCode: str = None
        self.settleBankName: str = None
        self.loanOrderType: str = None
