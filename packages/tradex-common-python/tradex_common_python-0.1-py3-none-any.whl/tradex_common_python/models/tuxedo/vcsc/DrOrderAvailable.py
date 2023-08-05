from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderAvailableReq(Request):
    __slots__ = 'accountNumber', 'password', 'code', 'sellBuyType', 'orderPrice', 'orderType'

    def __init__(self):
        super(DrOrderAvailableReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.code: str = ''
        self.sellBuyType: str = ''
        self.orderPrice: float = 0
        self.orderType: str = ''

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        data += self.code[:30].ljust(30, ' ')               # b_n03
        data += self.sellBuyType[:1].ljust(1, ' ')          # b_n04
        data += str(self.orderPrice or 0)[:12].ljust(12, ' ')         # b_n05
        data += self.orderType[:1].ljust(1, ' ')            # b_n06
        return data


class DrOrderAvailableRes(Base):
    __slots__ = 'availableQuantity', 'openPosition'

    def __init__(self):
        super(DrOrderAvailableRes, self).__init__()
        self.availableQuantity: int = None
        self.openPosition: int = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.availableQuantity = int(data[:8].decode().strip() or '0')
        instance.openPosition = int(data[8:16].decode().strip() or '0')
        return instance
