from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrAccountOpenPositionReq(Request):
    __slots__ = 'accountNumber', 'lastNextKey', 'fetchCount', 'password', 'branchCode', 'agencyCode', 'userName'

    def __init__(self):
        super(DrAccountOpenPositionReq, self).__init__()
        self.accountNumber: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None
        self.password: str = ''
        self.branchCode: str = ''
        self.agencyCode: str = ''
        self.userName: str = ''

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')             # b_n01
        data += self.password[:64].ljust(64, ' ')                 # b_n02
        data += self.branchCode[:3].ljust(3, ' ')             # b_n03
        data += self.agencyCode[:2].ljust(2, ' ')             # b_n04
        data += self.userName[:15].ljust(15, ' ')               # b_n05
        last_next_key = ''
        #  sprintf(ts_grdhdr,"%-s%-3s%-4s%-70s",(flags == QRY ? "0" : "2")," ","0",inext);
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n06
        return data


class DrAccountOpenPositionRes(Base):
    __slots__ = 'accountNumber', 'accountName', 'code', 'currencyCode', 'sellBuyType', 'quantity', \
                'previousQuantity', 'averagePrice', 'currentPrice', 'unrealizedPL', 'closableQuantity', \
                'tickSize', 'tickValue', 'priceAdjustment', 'nextKey'

    def __init__(self):
        super(DrAccountOpenPositionRes, self).__init__()
        self.code: str = None
        self.sellBuyType: str = None
        self.quantity: int = None
        self.previousQuantity: int = None
        self.averagePrice: float = None
        self.currentPrice: float = None
        self.unrealizedPL: float = None
        self.closableQuantity: int = None
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.accountNumber = data[:10].decode().strip()
        instance.accountName = data[10:110].decode().strip()
        instance.code = data[110:140].decode().strip()
        instance.currencyCode = data[140:143].decode().strip()
        instance.sellBuyType = data[143:144].decode().strip()
        instance.quantity = int(data[144:151].decode().strip() or '0')
        instance.previousQuantity = int(data[151:158].decode().strip() or '0')
        instance.averagePrice = float(data[158:173].decode().strip() or '0')
        instance.currentPrice = float(data[173:188].decode().strip() or '0')
        instance.unrealizedPL = float(data[188:209].decode().strip() or '0')
        instance.closableQuantity = int(data[209:216].decode().strip() or '0')
        instance.tickSize = float(data[216:228].decode().strip() or '0')
        instance.tickValue = float(data[228:240].decode().strip() or '0')
        instance.priceAdjustment = float(data[240:252].decode().strip() or '0')
        return instance
