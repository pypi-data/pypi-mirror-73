from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrWithdrawCashFeeReq(Request):
    __slots__ = 'sourceBank', 'destBank', 'amount', 'accountNumber'

    def __init__(self):
        super(DrWithdrawCashFeeReq, self).__init__()
        self.accountNumber: str = None
        self.sourceBank: str = None
        self.destBank: str = None
        self.amount: float = None


class DrWithdrawCashFeeRes(Base):
    __slots__ = 'feeAmount', 'paymentOnBehalf', 'adjustedAmount', 'feeType'

    def __init__(self):
        super(DrWithdrawCashFeeRes, self).__init__()
        self.feeAmount: float = None
        self.paymentOnBehalf: float = None
        self.adjustedAmount: float = None
        self.feeType: str = None
