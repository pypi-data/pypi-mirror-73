from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class LoanHistoryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'loanBankCode', 'lastLoanDate', 'lastLoanBankCode', \
                'lastMatchDate', 'lastStockCode', 'fetchCount'

    def __init__(self):
        super(LoanHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.loanBankCode: str = None
        self.lastLoanDate: str = None
        self.lastLoanBankCode: str = None
        self.lastMatchDate: str = None
        self.lastStockCode: str = None
        self.fetchCount: int = None


class LoanHistoryRes(Base):
    __slots__ = 'loanDate', 'matchDate', 'stockCode', 'matchQuantity', 'matchAmount', 'loanAmount', \
                'loanRepayAmount', 'loanRemainAmount', 'status', 'loanBankCode', 'loanBankName'

    def __init__(self):
        super(LoanHistoryRes, self).__init__()
        self.loanDate: str = None
        self.matchDate: str = None
        self.stockCode: str = None
        self.matchQuantity: int = None
        self.matchAmount: float = None
        self.loanAmount: float = None
        self.loanRepayAmount: float = None
        self.loanRemainAmount: float = None
        self.status: str = None
        self.loanBankCode: str = None
        self.loanBankName: str = None
