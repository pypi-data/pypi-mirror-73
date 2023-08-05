from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountCashBalanceReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'bankCode', 'bankAccount', 'bankName'

    def __init__(self):
        super(AccountCashBalanceReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.bankCode: str = None
        self.bankAccount: str = None
        self.bankName: str = None


class AccountCashBalanceRes(Base):
    __slots__ = 'depositAmount', 'depositBlockAmount', 'orderBlockAmount', 'stockEvaluationAmount', \
                'withdrawableAmount', 'reuseAmount', 'virtualDeposit', 'usedVirtualDeposit', \
                'marginLoanAmount', 'securedLoanAmount', 'expiredLoanAmount', 'waitSellAmount'

    def __init__(self):
        super(AccountCashBalanceRes, self).__init__()
        self.depositAmount: float = None
        self.depositBlockAmount: float = None
        self.orderBlockAmount: float = None
        self.stockEvaluationAmount: float = None
        self.withdrawableAmount: float = None
        self.reuseAmount: float = None
        self.virtualDeposit: float = None
        self.usedVirtualDeposit: float = None
        self.marginLoanAmount: float = None
        self.securedLoanAmount: float = None
        self.expiredLoanAmount: float = None
        self.waitSellAmount: float = None

