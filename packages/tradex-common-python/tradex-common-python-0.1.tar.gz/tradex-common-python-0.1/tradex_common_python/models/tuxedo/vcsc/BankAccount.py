from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class BankAccountReq(Request):
    __slots__ = 'accountNumber', 'subNumber'

    def __init__(self):
        super(BankAccountReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None


class BankAccountRes(Base):
    __slots__ = 'bankCode', 'bankName', 'bankAccount'

    def __init__(self):
        super(BankAccountRes, self).__init__()
        self.bankCode: str = None
        self.bankName: str = None
        self.bankAccount: int = None
