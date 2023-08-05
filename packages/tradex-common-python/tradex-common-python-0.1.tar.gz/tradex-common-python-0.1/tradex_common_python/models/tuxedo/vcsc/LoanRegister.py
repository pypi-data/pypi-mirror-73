from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class LoanRegisterReq(Request):
    __slots__ = 'items'

    def __init__(self):
        super(LoanRegisterReq, self).__init__()
        self.items: [LoanRegisterItemReq] = None


class LoanRegisterItemReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'loanBankCode', 'settleBankCode', 'matchDate', 'settleDate', \
                'stockCode', 'matchQuantity', 'matchAmount', 'tradingFee', 'adjustAmount', 'possibleAmount', \
                'loanAmount', 'feeRate', 'tax', 'loanOrderType'

    def __init__(self):
        super(LoanRegisterItemReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.loanBankCode: str = None
        self.settleBankCode: str = None
        self.matchDate: str = None
        self.settleDate: str = None
        self.stockCode: str = None
        self.matchQuantity: int = None
        self.matchAmount: float = None
        self.tradingFee: float = None
        self.tax: float = None
        self.adjustAmount: float = None
        self.possibleAmount: float = None
        self.loanAmount: float = None
        self.feeRate: float = None
        self.loanOrderType: str = None


class LoanRegisterRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(LoanRegisterRes, self).__init__()
        self.message: str = None
