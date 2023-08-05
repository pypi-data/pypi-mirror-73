from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrTransferCashInfoReq(Request):
    __slots__ = 'accountNumber', 'subNumber'

    def __init__(self):
        super(DrTransferCashInfoReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None


class DrTransferCashInfoRes(Base):
    __slots__ = 'depositAmount', 'waitingAmount', 'transferableAmount'

    def __init__(self):
        super(DrTransferCashInfoRes, self).__init__()
        self.depositAmount: float = None
        self.waitingAmount: float = None
        self.transferableAmount: float = None
