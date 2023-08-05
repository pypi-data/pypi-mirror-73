from tradex_common_python.models.Constants import SellBuyTypeEnum
from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderMatchReq(Request):
    __slots__ = 'accountNumber', 'password', 'favoriteListGroupName', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrOrderMatchReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.favoriteListGroupName: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        data += self.favoriteListGroupName[:20].ljust(20, ' ')                 # b_n03
        last_next_key = ''
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n04
        return data


class DrOrderMatchRes(Base):
    __slots__ = 'accountNumber', 'accountName', 'orderNumber', 'code', 'sellBuyType', 'matchPrice', \
                'matchedQuantity',  'unmatchedQuantity', 'time', 'liquidationPositionNumber', 'nextKey'

    def __init__(self):
        super(DrOrderMatchRes, self).__init__()
        self.accountNumber: str = None
        self.accountName: str = None
        self.orderNumber: str = None
        self.code: str = None
        self.sellBuyType: str = None
        self.matchPrice: float = None
        self.matchedQuantity: int = None
        self.unmatchedQuantity: int = None
        self.time: str = None
        self.liquidationPositionNumber: int = None
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.accountNumber: str = data[:10].decode().strip()
        instance.accountName = data[10:110].decode().strip()
        instance.orderNumber = data[110:117].decode().strip()
        instance.code = data[117:147].decode().strip()
        instance.sellBuyType = data[147:148].decode().strip()
        instance.matchPrice = float(data[148:163].decode().strip() or '0')
        instance.matchedQuantity = int(data[163:170].decode().strip() or '0')
        instance.unmatchedQuantity = int(data[170:177].decode().strip() or '0')
        instance.time = data[177:193].decode().strip()
        instance.liquidationPositionNumber = data[193:206].decode().strip()

        instance.sellBuyType = SellBuyTypeEnum(instance.sellBuyType).name
        return instance
