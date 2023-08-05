from typing import List

from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrHistoryTradeReq(Request):
    __slots__ = 'fromDate', 'toDate', 'accountNumber', 'password', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrHistoryTradeReq, self).__init__()
        self.fromDate: str = ''
        self.toDate: str = ''
        self.accountNumber: str = ''
        self.password: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None

    def to_string(self) -> str:
        data = self.fromDate[:8].ljust(8, ' ')              # b_n01
        data += self.toDate[:8].ljust(8, ' ')               # b_n02
        data += self.accountNumber[:10].ljust(10, ' ')       # b_n03
        data += self.password[:64].ljust(64, ' ')            # b_n04
        last_next_key = ''
        #  sprintf(ts_grdhdr,"%-s%-3s%-4s%-70s",(flags == QRY ? "0" : "2")," ","0",inext);
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n05
        return data


class DrHistoryTradeRes(Base):
    __slots__ = 'totalBuyQuantity', 'totalSellQuantity', 'totalQuantity', 'totalFee', 'totalTax', 'items', 'nextKey'

    def __init__(self):
        super(DrHistoryTradeRes, self).__init__()
        self.totalBuyQuantity: int = None
        self.totalSellQuantity: int = None
        self.totalQuantity: int = None
        self.totalFee: float = None
        self.totalTax: int = None
        self.items: List[DrHistoryTradeItem] = list()
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.totalBuyQuantity = int(data[:7].decode().strip() or '0')
        instance.totalSellQuantity = int(data[7:14].decode().strip() or '0')
        instance.totalQuantity = int(data[14:21].decode().strip() or '0')
        instance.totalFee = float(data[21:36].decode().strip() or '0')
        instance.totalTax = float(data[36:51].decode().strip() or '0')
        return instance


class DrHistoryTradeItem(Base):
    __slots__ = 'accountNumber', 'accountName', 'tradingDate', 'orderNumber', 'originalOrderNumber', 'code',\
                'sellBuyType', 'orderQuantity', 'matchedPrice', 'matchedQuantity', 'tradingAmount', 'commission',\
                'tax', 'tradingChannel', 'userId', 'orderDate', 'userIp'

    def __init__(self):
        super(DrHistoryTradeItem, self).__init__()
        self.accountNumber: str = None
        self.accountName: str = None
        self.tradingDate: str = None
        self.orderNumber: str = None
        self.originalOrderNumber: str = None
        self.code: str = None
        self.sellBuyType: str = None
        self.orderQuantity: int = None
        self.matchedPrice: float = None
        self.matchedQuantity: int = None
        self.tradingAmount: float = None
        self.commission: str = None
        self.tax: float = None
        self.tradingChannel: str = None
        self.userId: str = None
        self.orderDate: str = None
        self.userIp: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.accountNumber = data[:10].decode().strip()
        instance.accountName = data[10:110].decode().strip()
        instance.tradingDate = data[110:118].decode().strip()
        instance.orderNumber = data[118:125].decode().strip()
        instance.originalOrderNumber = data[125:132].decode().strip()
        instance.code = data[132:162].decode().strip()
        instance.sellBuyType = data[162:163].decode().strip()
        instance.orderQuantity = float(data[163:170].decode().strip() or '0')
        instance.matchedPrice = float(data[170:185].decode().strip() or '0')
        instance.matchedQuantity = float(data[185:192].decode().strip() or '0')
        instance.tradingAmount = float(data[192:207].decode().strip() or '0')
        instance.commission = data[207:222].decode().strip()
        instance.tax = float(data[222:237].decode().strip() or '0')
        instance.tradingChannel = data[237:245].decode().strip()
        instance.userId = data[245:260].decode().strip()
        instance.orderDate = data[260:268].decode().strip()
        instance.userIp = data[268:283].decode().strip()
        return instance
