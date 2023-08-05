from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrImDepositInfoReq(Request):
    __slots__ = 'accountNumber', 'subNumber'

    def __init__(self):
        super(DrImDepositInfoReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None


class DrImDepositInfoRes(Base):
    __slots__ = 'depositAmount', 'otherBlockAmount', 'collateralAmount', 'withdrawBlockAmount', 'depositBlockAmount', \
                'availableAmount', 'settleBlockAmount', 'maturityBlockAmount'

    def __init__(self):
        super(DrImDepositInfoRes, self).__init__()
        self.depositAmount: float = None
        self.otherBlockAmount: float = None
        self.collateralAmount: float = None
        self.withdrawBlockAmount: float = None
        self.depositBlockAmount: float = None
        self.availableAmount: float = None
        self.settleBlockAmount: float = None
        self.maturityBlockAmount: float = None
