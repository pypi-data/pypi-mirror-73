from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrAccountSummaryReq(Request):
    __slots__ = 'accountNumber', 'password'

    def __init__(self):
        super(DrAccountSummaryReq, self).__init__()
        self.accountNumber: str = None
        self.password: str = None

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        return data


class DrAccountSummaryRes(Base):
    __slots__ = 'date', 'previousCashBalance', 'todayCashBalance', 'inOutAmount', 'pendingWithdrawalAmount', \
                'CAA', 'pendingWithdrawalCAA', 'assetCollateralValue', 'realizedPL', 'unrealizedPL', 'assignedFee', \
                'fee', 'tax', 'marginRequirement', 'secMarginRequirement', 'unmatchedOrderMarginRequirement', \
                'marginUtilization', 'marginDeficit', 'availableFundForWithdraw', 'availableFundForOrder', \
                'availableFundForWithdrawCAA'

    def __init__(self):
        super(DrAccountSummaryRes, self).__init__()
        self.date: str = None
        self.previousCashBalance: float = None
        self.todayCashBalance: float = None
        self.inOutAmount: float = None
        self.pendingWithdrawalAmount: float = None
        self.CAA: float = None
        self.pendingWithdrawalCAA: float = None
        self.assetCollateralValue: float = None
        self.realizedPL: float = None
        self.unrealizedPL: float = None
        self.assignedFee: float = None
        self.fee: float = None
        self.tax: float = None
        self.marginRequirement: float = None
        self.secMarginRequirement: float = None
        self.unmatchedOrderMarginRequirement: float = None
        self.marginUtilization: float = None
        self.marginDeficit: float = None
        self.availableFundForWithdraw: float = None
        self.availableFundForOrder: float = None
        self.availableFundForWithdrawCAA: float = None
