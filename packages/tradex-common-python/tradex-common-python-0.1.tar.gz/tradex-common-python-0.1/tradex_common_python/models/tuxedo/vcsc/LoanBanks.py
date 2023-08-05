from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class LoanBanksReq(Request):
    __slots__ = 'lastBankCode', 'fetchCount'

    def __init__(self):
        super(LoanBanksReq, self).__init__()
        self.lastBankCode: str = None
        self.fetchCount: int = None


class LoanBanksRes(Base):
    __slots__ = 'bankCode', 'bankName'

    def __init__(self):
        super(LoanBanksRes, self).__init__()
        self.bankCode: str = None
        self.bankName: str = None
