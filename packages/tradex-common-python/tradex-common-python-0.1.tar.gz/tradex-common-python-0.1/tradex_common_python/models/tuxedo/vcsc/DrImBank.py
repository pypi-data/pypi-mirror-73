from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrImBankReq(Request):
    __slots__ = 'accountNumber', 'type'

    def __init__(self):
        super(DrImBankReq, self).__init__()
        self.accountNumber: str = None
        self.type: str = None


class DrImBankRes(Base):
    __slots__ = 'bankAccountNumber', 'bankAccountName'

    def __init__(self):
        super(DrImBankRes, self).__init__()
        self.bankAccountNumber: str = None
        self.bankAccountName: str = None
