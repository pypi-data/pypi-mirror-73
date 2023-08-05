from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderModifyReq(Request):
    __slots__ = 'accountNumber', 'code', 'orderQuantity', 'orderPrice', 'orderNumber', 'unmatchedQuantity', \
                'orderType', 'password', 'validity', 'stopPrice', 'regYn', 'hegYn'

    def __init__(self):
        super(DrOrderModifyReq, self).__init__()
        self.accountNumber: str = ''
        self.code: str = ''
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.orderNumber: str = ''
        self.orderType: str = ''
        self.unmatchedQuantity: int = None
        self.password: str = ''
        self.validity: str = ''
        self.stopPrice: str = ''
        self.regYn: str = ''
        self.hegYn: str = ''

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')     # b_n01 - AccountNumber
        data += self.password[:64].ljust(64, ' ')         # b_n02 - Password
        data += '2'                                       # b_n03 - Modify Cancel type (2:Modify 3:Cancel )
        data += self.orderNumber[:7].ljust(7, ' ')        # b_n04 - OrderNumber
        data += self.code[:30].ljust(30, ' ')             # b_n05 - Code
        data += self.orderType[:1].ljust(1, ' ')          # b_n06 - OrderType
        data += self.validity[:1].ljust(1, ' ')           # b_n07 - Validity  O.DAY 2.ATO 3.IOC 4.FOK 7.ATC
        data += str(self.orderQuantity or 0)[:8].ljust(8, ' ')      # b_n08 - OrderQuantity
        data += str(self.unmatchedQuantity or 0)[:8].ljust(8, ' ')  # b_n09 - UnMatchedQuantity
        data += str(self.orderPrice or 0)[:12].ljust(12, ' ')       # b_n10 - OrderPrice
        data += self.stopPrice.ljust(12, ' ')                        # b_n11 - Stop Order Price
        data += self.regYn.ljust(1, ' ')                         # b_n12 - Option Y/N
        data += self.hegYn.ljust(1, ' ')                         # b_n13 - Hedge
        return data


class DrOrderModifyRes(Base):
    __slots__ = 'orderNumber'

    def __init__(self):
        super(DrOrderModifyRes, self).__init__()
        self.orderNumber: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.orderNumber = data[:7].decode().strip()
        return instance
