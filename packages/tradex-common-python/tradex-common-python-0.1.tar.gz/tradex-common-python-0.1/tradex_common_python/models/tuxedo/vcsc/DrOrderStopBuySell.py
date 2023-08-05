from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderStopBuySellReq(Request):
    __slots__ = 'date', 'accountNumber', 'password', 'code', 'sellBuyType', 'orderType', 'orderValidity', \
                'orderQuantity', 'orderPrice', 'bandPrice', 'fromDate', 'toDate', 'stopPrice'

    def __init__(self):
        super(DrOrderStopBuySellReq, self).__init__()
        self.date: str = ''
        self.accountNumber: str = ''
        self.password: str = ''
        self.code: str = ''
        self.sellBuyType: str = ''
        self.orderType: str = ''
        self.orderValidity: str = ''
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.bandPrice: float = None
        self.fromDate: str = ''
        self.toDate: str = ''
        self.stopPrice: float = None  # addition field (active price)

    def to_string(self) -> str:
        data = self.date[:8].ljust(8, ' ')                  # b_n01
        data += self.accountNumber[:10].ljust(10, ' ')      # b_n02
        data += self.password[:64].ljust(64, ' ')           # b_n03
        data += self.code[:30].ljust(30, ' ')               # b_n04
        data += self.sellBuyType[:1].ljust(1, ' ')          # b_n05
        data += self.orderType[:1].ljust(1, ' ')            # b_n06
        data += self.orderValidity[:1].ljust(1, ' ')        # b_n07
        data += str(self.orderQuantity or 0)[:7].rjust(7, '0')        # b_n08
        data += str(self.orderPrice or 0)[:15].ljust(15, ' ')         # b_n09
        data += str(self.bandPrice or 0)[:15].ljust(15, ' ')          # b_n10
        data += self.fromDate[:8].ljust(8, ' ')            # b_n11
        data += self.toDate[:8].ljust(8, ' ')              # b_n12
        return data


class DrOrderStopBuySellRes(Base):
    __slots__ = 'dummy'

    def __init__(self):
        super(DrOrderStopBuySellRes, self).__init__()
        self.dummy: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.dummy = data[:1].decode().strip()
        return instance
