from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountLoanHistoryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'nextKey', 'fetchCount'

    def __init__(self):
        super(AccountLoanHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.nextKey: str = None
        self.fetchCount: int = None


class AccountLoanHistoryRes(Base):
    __slots__ = 'loanDate', 'expiredDate', 'stockCode', 'loanType', 'loanQuantity', 'loanAmount', \
                'loanInterest', 'loanRepayAmount', 'loanRemainAmount', 'status', 'nextKey'

    def __init__(self):
        super(AccountLoanHistoryRes, self).__init__()
        self.loanDate: str = None
        self.expiredDate: str = None
        self.stockCode: str = None
        self.loanType: str = None
        self.loanQuantity: int = None
        self.loanAmount: float = None
        self.loanInterest: float = None
        self.loanRepayAmount: float = None
        self.loanRemainAmount: float = None
        self.status: str = None
        self.nextKey: str = None
