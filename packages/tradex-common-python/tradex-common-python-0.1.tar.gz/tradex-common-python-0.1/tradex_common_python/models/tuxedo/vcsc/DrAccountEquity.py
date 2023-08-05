from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrAccountEquityReq(Request):
    __slots__ = 'accountNumber'

    def __init__(self):
        super(DrAccountEquityReq, self).__init__()
        self.accountNumber: str = None


class DrAccountEquityRes(Base):
    __slots__ = 'availableCashBalance', 'totalCashBalance', 'availableStockQuantity', 'availableStockAmount', \
                'totalStockQuantity', 'totalStockAmount'

    def __init__(self):
        super(DrAccountEquityRes, self).__init__()
        self.availableCashBalance: float = None
        self.totalCashBalance: float = None
        self.availableStockQuantity: float = None
        self.availableStockAmount: float = None
        self.totalStockQuantity: float = None
        self.totalStockAmount: float = None
