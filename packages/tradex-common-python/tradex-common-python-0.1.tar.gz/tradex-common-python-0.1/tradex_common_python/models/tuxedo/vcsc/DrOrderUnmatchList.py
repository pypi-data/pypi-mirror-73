from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderUnmatchListReq(Request):
    __slots__ = 'accountNumber', 'password', 'groupName', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrOrderUnmatchListReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.groupName: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        data += self.groupName[:20].ljust(20, ' ')          # b_n03
        data += self.lastNextKey[:78].ljust(78, ' ')            # b_n04
        return data


class DrOrderUnmatchListRes(Base):
    __slots__ = 'accountNumber', 'accountName', 'orderNumber', 'orderStatus', 'strategyType', 'orderType', 'code', \
                'sellBuyType', 'orderQuantity', 'orderPrice', 'matchedQuantity', 'unmatchedQuantity',\
                'validity', 'orderStyle', 'nextKey'

    def __init__(self):
        super(DrOrderUnmatchListRes, self).__init__()
        self.accountNumber: str = None
        self.accountName: str = None
        self.orderNumber: str = None
        self.orderStatus: str = None
        self.strategyType: str = None
        self.orderType: str = None
        self.code: str = None
        self.sellBuyType: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.matchedQuantity: int = None
        self.unmatchedQuantity: int = None
        self.validity: str = None
        self.orderStyle: str = None
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.accountNumber = data[:10].decode().strip()
        instance.accountName = data[10:110].decode().strip()
        instance.orderNumber = data[110:117].decode().strip()
        instance.orderStatus = data[117:147].decode().strip()
        instance.strategyType = data[147:148].decode().strip()
        instance.orderType = data[148:149].decode().strip()
        instance.code = data[149:179].decode().strip()
        instance.sellBuyType = data[179:180].decode().strip()
        instance.orderQuantity = int(data[180:187].decode().strip())
        instance.orderPrice = float(data[187:202].decode().strip())
        instance.matchedQuantity = int(data[202:209].decode().strip())
        instance.unmatchedQuantity = int(data[209:216].decode().strip())
        instance.validity = data[216:217].decode().strip()
        instance.orderStyle = data[217:218].decode().strip()
        return instance
