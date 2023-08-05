from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderPlaceReq(Request):
    __slots__ = 'accountNumber', 'password', 'code', 'sellBuyType', 'orderType', 'orderCondition', 'orderQuantity', \
                'orderPrice', 'stopOrderPrice', 'date', 'regYn', 'hegYn', 'minMatchQuantity'

    def __init__(self):
        super(DrOrderPlaceReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.code: str = ''
        self.sellBuyType: str = ''
        self.orderType: str = ''
        self.orderCondition: str = ''
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.stopOrderPrice: str = ''
        self.regYn: str = ''
        self.hegYn: str = ''
        self.minMatchQuantity: str = ''

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')           # b_n01 - AccountNumber
        data += self.password[:64].ljust(64, ' ')               # b_n02 - Password
        data += self.code[:30].ljust(30, ' ')                   # b_n03 - Code
        data += self.sellBuyType[:1].ljust(1, ' ')              # b_n04 - SellBuyType
        data += self.orderType[:1].ljust(1, ' ')                # b_n05 - OrderType
        data += self.orderCondition[:1].ljust(1, ' ')           # b_n06 - OrderCondition
        data += str(self.orderQuantity or 0)[:8].rjust(8, '0')  # b_n07 - OrderQuantity
        data += str(self.orderPrice or 0)[:12].ljust(12, ' ')   # b_n08 - OrderPrice
        data += str(self.stopOrderPrice or 0).ljust(12, ' ')    # b_n09 - StopOrderPrice = 0
        data += self.date.ljust(8, ' ')                         # b_n10 - vaildDate = null
        data += self.regYn.ljust(1, ' ')                        # b_n11 - Option Y/N = N
        data += self.hegYn.ljust(1, ' ')                        # b_n12 - Hedge = 0
        data += str(self.minMatchQuantity or 0).ljust(8, '0')   # b_n13 - Min Match Qty : Only user for IOC = 0
        return data


class DrOrderPlaceRes(Base):
    __slots__ = 'orderNumber'

    def __init__(self):
        super(DrOrderPlaceRes, self).__init__()
        self.orderNumber: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.orderNumber = data[:7].decode().strip()
        return instance
