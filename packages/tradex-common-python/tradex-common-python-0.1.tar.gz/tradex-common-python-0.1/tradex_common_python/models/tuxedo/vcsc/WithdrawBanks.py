from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class WithdrawBanksReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'fetchCount'

    def __init__(self):
        super(WithdrawBanksReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.fetchCount: int = None


class WithdrawBanksRes(Base):
    __slots__ = 'bankCode', 'bankName', 'bankAccountNumber', 'bankAccountName'

    def __init__(self):
        super(WithdrawBanksRes, self).__init__()
        self.bankCode: str = None
        self.bankName: str = None
        self.bankAccountNumber: str = None
        self.bankAccountName: str = None
