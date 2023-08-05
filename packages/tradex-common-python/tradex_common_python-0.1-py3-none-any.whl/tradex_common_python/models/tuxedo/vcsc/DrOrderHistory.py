from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderHistoryReq(Request):
    __slots__ = 'accountNumber', 'password', 'date', 'lastNextKey', 'fetchCount',\
                'branchCode', 'agencyCode', 'empGroupId'

    def __init__(self):
        super(DrOrderHistoryReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.date: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None
        self.branchCode: str = ''  # only for kis
        self.agencyCode: str = ''  # only for kis
        self.empGroupId: str = ''  # only for kis

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        data += self.date[:8].ljust(8, ' ')                 # b_n03
        last_next_key = ''
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n04
        return data

    def to_kis_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')
        data += self.password[:64].ljust(64, ' ')
        data += self.branchCode[:3].ljust(3, ' ')
        data += self.agencyCode[:2].ljust(2, ' ')
        last_next_key = ''
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n04
        return data


class DrOrderHistoryRes(Base):
    __slots__ = 'orderNumber', 'originalOrderNumber', 'modifyCancelType', 'code', 'sellBuyType', 'orderQuantity', \
                'matchedQuantity',  'unmatchedQuantity', 'orderType', 'orderPrice', 'orderDate', 'orderTime', \
                'validity', 'hegYn', 'userId', 'rejectionMessage', 'nextKey', \
                'accountNumber', 'accountName', 'strategyType', 'cancelQuantity', 'orderStyle'

    def __init__(self):
        super(DrOrderHistoryRes, self).__init__()
        self.orderNumber: str = None
        self.originalOrderNumber: str = None
        self.modifyCancelType: str = None
        self.code: str = None
        self.sellBuyType: str = None
        self.orderQuantity: int = None
        self.matchedQuantity: int = None
        self.unmatchedQuantity: int = None
        self.orderType: str = None
        self.orderPrice: float = None
        self.orderTime: str = None
        self.validity: str = None
        self.hegYn: str = None
        self.userId: str = None
        self.rejectionMessage: str = None
        self.orderDate: str = None          # Additional field
        self.nextKey: str = None            # Additional field
        self.accountNumber: str = None              # only for kis
        self.accountName: str = None                # only for kis
        self.strategyType: str = None               # only for kis
        self.cancelQuantity: int = None             # only for kis
        self.orderStyle: str = None                 # only for kis

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.orderNumber: str = data[:7].decode().strip()
        instance.originalOrderNumber = data[7:14].decode().strip()
        instance.modifyCancelType = data[14:44].decode().strip()
        instance.code = data[44:74].decode().strip()
        instance.sellBuyType = data[74:75].decode().strip()
        instance.orderQuantity = int(data[75:82].decode().strip() or '0')
        instance.matchedQuantity = int(data[82:89].decode().strip() or '0')
        instance.unmatchedQuantity = int(data[89:96].decode().strip() or '0')
        instance.orderType = data[96:97].decode().strip()
        instance.orderPrice = float(data[97:112].decode().strip() or '0')
        instance.orderDate = data[112:120].decode().strip()
        instance.orderTime = data[120:126].decode().strip()
        instance.validity = data[126:127].decode().strip()
        instance.hegYn = data[127:128].decode().strip()
        instance.userId = data[128:143].decode().strip()
        instance.rejectionMessage = data[143:223].decode().strip()
        return instance

    @classmethod
    def from_kis_bytes(cls, data: bytes):
        instance = cls()
        instance.accountNumber = data[:10].decode().strip()
        instance.accountName = data[10:110].decode().strip()
        instance.orderNumber = data[110: 117].decode().strip()
        instance.originalOrderNumber = data[117: 124].decode().strip()
        instance.modifyCancelType = data[124: 154].decode().strip()
        instance.strategyType = data[154: 155].decode().strip()
        instance.code = data[155: 185].decode().strip()
        instance.sellBuyType = data[185: 186].decode().strip()
        instance.orderQuantity = int(data[186:193].decode().strip() or '0')
        instance.matchedQuantity = int(data[193:200].decode().strip() or '0')
        instance.unmatchedQuantity = int(data[200:207].decode().strip() or '0')
        instance.cancelQuantity = int(data[207:214].decode().strip() or '0')
        instance.orderType = data[214:215].decode().strip()
        instance.orderPrice = float(data[215:230].decode().strip() or '0')
        instance.orderTime = data[230:238].decode().strip()
        instance.userId = data[238:258].decode().strip()
        instance.validity = data[258:259].decode().strip()
        instance.orderStyle = data[259:260].decode().strip()
        instance.rejectionMessage = data[260:360].decode().strip()
        return instance
