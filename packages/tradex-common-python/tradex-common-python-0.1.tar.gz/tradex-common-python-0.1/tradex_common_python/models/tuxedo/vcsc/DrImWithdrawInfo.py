from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrImWithdrawInfoReq(Request):
    __slots__ = 'accountNumber', 'subNumber'

    def __init__(self):
        super(DrImWithdrawInfoReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None


class DrImWithdrawInfoRes(Base):
    __slots__ = 'depositAmount', 'otherBlockAmount', 'collateralAmount', 'withdrawBlockAmount', 'depositBlockAmount', \
                'availableAmount', 'settleBlockAmount'

    def __init__(self):
        super(DrImWithdrawInfoRes, self).__init__()
        self.depositAmount: float = None
        self.otherBlockAmount: float = None
        self.collateralAmount: float = None
        self.withdrawBlockAmount: float = None
        self.depositBlockAmount: float = None
        self.availableAmount: float = None
        self.settleBlockAmount: float = None
