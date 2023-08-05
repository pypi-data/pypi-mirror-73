from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrAccountUnmatchPositionReq(Request):
    __slots__ = 'accountNumber', 'password', 'code', 'sellBuyType', 'limitPrice', 'orderType', 'stopPrice'

    def __init__(self):
        super(DrAccountUnmatchPositionReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.code: str = ''
        self.sellBuyType: str = None
        self.limitPrice: float = None
        self.orderType: str = None
        self.stopPrice: float = None

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        data += self.code[:30].ljust(30, ' ')               # b_n03
        data += self.sellBuyType[:1].ljust(1, ' ')          # b_n04
        data += str(self.limitPrice or '')[:12].ljust(12, ' ')         # b_n05
        data += self.orderType[:1].ljust(1, ' ')                       # b_n06
        data += str(self.stopPrice or '')[:12].ljust(12, ' ')          # b_n07
        return data


class DrAccountUnmatchPositionRes(Base):
    __slots__ = 'nonSettledBuyQuantity', 'nonSettledSellQuantity', 'UnmatchedBuyQuantity', 'UnmatchedSellQuantity'

    def __init__(self):
        super(DrAccountUnmatchPositionRes, self).__init__()
        self.nonSettledBuyQuantity: int = None
        self.nonSettledSellQuantity: int = None
        self.UnmatchedBuyQuantity: int = None
        self.UnmatchedSellQuantity: int = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.nonSettledBuyQuantity = int(data[:8].decode().strip() or '0')
        instance.nonSettledSellQuantity = int(data[8:16].decode().strip() or '0')
        instance.UnmatchedBuyQuantity = int(data[16:24].decode().strip() or '0')
        instance.UnmatchedSellQuantity = int(data[24:32].decode().strip() or '0')
        return instance
