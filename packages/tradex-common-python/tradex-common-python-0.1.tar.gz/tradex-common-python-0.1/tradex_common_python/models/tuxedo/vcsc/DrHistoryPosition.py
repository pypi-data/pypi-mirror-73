from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrHistoryPositionReq(Request):
    __slots__ = 'accountNumber', 'password', 'fromDate', 'toDate', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrHistoryPositionReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.fromDate: str = ''
        self.toDate: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')                   # b_n01
        data += self.password[:64].ljust(64, ' ')                       # b_n02
        data += self.fromDate[:8].ljust(8, ' ')                         # b_n03
        data += self.toDate[:8].ljust(8, ' ')                           # b_n04
        last_next_key = ''
        #  sprintf(ts_grdhdr,"%-s%-3s%-4s%-70s",(flags == QRY ? "0" : "2")," ","0",inext);
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n05
        return data


class DrHistoryPositionRes(Base):
    __slots__ = 'tradingDate', 'maturityDate', 'code', 'sellBuyType', 'quantity', 'matchPrice', \
                'lastPrice', 'unrealizedPL', 'nextKey', 'accountNumber', 'accountName', 'userId'

    def __init__(self):
        super(DrHistoryPositionRes, self).__init__()
        self.tradingDate: str = None
        self.accountNumber: str = None
        self.accountName: str = None
        self.maturityDate: str = None
        self.code: str = None
        self.sellBuyType: str = None
        self.quantity: int = None
        self.matchPrice: float = None
        self.lastPrice: float = None
        self.unrealizedPL: float = None
        self.nextKey: str = None
        self.userId: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.tradingDate = data[:8].decode().strip()
        instance.accountNumber = data[8:18].decode().strip()
        instance.accountName = data[18:118].decode().strip()
        instance.code = data[118:148].decode().strip()
        instance.sellBuyType = data[148:149].decode().strip()
        instance.quantity = data[149:156].decode().strip()
        instance.matchPrice = data[156:171].decode().strip()
        instance.lastPrice = data[171:186].decode().strip()
        instance.unrealizedPL = data[186:207].decode().strip()
        instance.maturityDate = data[207:215].decode().strip()
        instance.userId = data[215:230].decode().strip()
        return instance
