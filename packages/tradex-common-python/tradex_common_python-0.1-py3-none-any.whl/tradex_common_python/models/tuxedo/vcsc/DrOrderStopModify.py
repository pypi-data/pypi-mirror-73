from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderStopModifyReq(Request):
    __slots__ = 'createdDate', 'sequenceNumber', 'accountNumber', 'password', 'orderQuantity', 'bandPrice', \
                'orderPrice', 'fromDate', 'toDate', 'stopPrice'

    def __init__(self):
        super(DrOrderStopModifyReq, self).__init__()
        self.createdDate: str = ''
        self.sequenceNumber: str = ''
        self.accountNumber: str = ''
        self.password: str = ''
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.bandPrice: float = None
        self.stopPrice: float = None    # additional field
        self.fromDate: str = ''
        self.toDate: str = ''

    def to_string(self) -> str:
        data = self.createdDate[:8].ljust(8, ' ')                  # b_n01
        data += self.sequenceNumber[:15].ljust(15, ' ')     # b_n02
        data += self.accountNumber[:10].ljust(10, ' ')      # b_n03
        data += self.password[:64].ljust(64, ' ')           # b_n04
        data += str(self.orderQuantity or 0)[:7].ljust(7, ' ')        # b_n05
        data += str(self.orderPrice or 0)[:15].ljust(15, ' ')          # b_n07
        data += str(self.bandPrice or 0)[:15].ljust(15, ' ')         # b_n06
        data += self.fromDate[:8].ljust(8, ' ')            # b_n08
        data += self.toDate[:8].ljust(8, ' ')              # b_n09
        return data


class DrOrderStopModifyRes(Base):
    __slots__ = 'dummy'

    def __init__(self):
        super(DrOrderStopModifyRes, self).__init__()
        self.dummy: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.dummy = data[:1].decode().strip()
        return instance
