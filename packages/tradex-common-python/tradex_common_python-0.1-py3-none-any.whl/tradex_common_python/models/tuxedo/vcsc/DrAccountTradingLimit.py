from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrAccountTradingLimitReq(Request):
    __slots__ = 'accountNumber', 'password', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrAccountTradingLimitReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        last_next_key = ''
        #  sprintf(ts_grdhdr,"%-s%-3s%-4s%-70s",(flags == QRY ? "0" : "2")," ","0",inext);
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n03
        return data


class DrAccountTradingLimitRes(Base):
    __slots__ = 'accountNumber', 'accountName', 'code', 'tradingLimit', 'tradingLimitYn', 'tickLimit', \
                'tickLimitYn', 'useTradingLimitYn', 'nextKey'

    def __init__(self):
        super(DrAccountTradingLimitRes, self).__init__()
        self.accountNumber: str = None
        self.accountName: str = None
        self.code: str = None
        self.tradingLimit: float = None
        self.tradingLimitYn: bool = None
        self.tickLimit: float = None
        self.tickLimitYn: bool = None
        self.useTradingLimitYn: bool = None
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.accountNumber = data[:10].decode().strip()
        instance.accountName = data[10:110].decode().strip()
        instance.code = data[110:120].decode().strip()
        instance.tradingLimit = float(data[120:129].decode().strip() or '0')
        instance.tradingLimitYn = data[129:139].decode().strip()
        instance.tickLimit = float(data[139:148].decode().strip() or '0')
        instance.tickLimitYn = data[148:158].decode().strip()
        instance.useTradingLimitYn = data[158:168].decode().strip()
        return instance
