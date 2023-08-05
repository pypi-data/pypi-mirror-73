from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrCashWithdrawInfoReq(Request):
    __slots__ = 'accountNumber'

    def __init__(self):
        super(DrCashWithdrawInfoReq, self).__init__()
        self.accountNumber: str = None


class DrCashWithdrawInfoRes(Base):
    __slots__ = 'depositAmount', 'totalBlockAmount', 'waitingAmount', 'withdrawableAmount', 'depositBlockAmount', \
                'fillingLossBlockAmount', 'maturityPaymentBlockAmount'

    def __init__(self):
        super(DrCashWithdrawInfoRes, self).__init__()
        self.depositAmount: float = None
        self.totalBlockAmount: float = None
        self.waitingAmount: float = None
        self.withdrawableAmount: float = None
        self.depositBlockAmount: float = None
        self.fillingLossBlockAmount: float = None
        self.maturityPaymentBlockAmount: float = None
