from typing import List

from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrHistoryClosedPositionReq(Request):
    __slots__ = 'fromDate', 'toDate', 'accountNumber', 'password', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrHistoryClosedPositionReq, self).__init__()
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


class DrHistoryClosedPositionRes(Base):
    __slots__ = 'totalQuantity', 'totalRealizedPl', 'totalFee', 'totalNetProfitLoss', 'closedPositionItems', 'nextKey'

    def __init__(self):
        super(DrHistoryClosedPositionRes, self).__init__()
        self.totalQuantity: int = None
        self.totalRealizedPl: float = None
        self.totalFee: float = None
        self.totalNetProfitLoss: float = None
        self.closedPositionItems: List[DrHistoryClosedPositionItem] = list()
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.totalQuantity = int(data[:7].decode().strip() or '0')
        instance.totalRealizedPl = float(data[7:28].decode().strip() or '0')
        instance.totalFee = float(data[28:43].decode().strip() or '0')
        instance.totalNetProfitLoss = float(data[43:64].decode().strip() or '0')
        return instance


class DrHistoryClosedPositionItem(Base):
    __slots__ = 'closeDate', 'accountNumber', 'accountName', 'code', 'matchedQuantity', 'buyPrice', 'sellPrice', \
                'realizedPl', 'commission', 'netProfitLoss', 'userId', 'nextKey'

    def __init__(self):
        super(DrHistoryClosedPositionItem, self).__init__()
        self.closeDate: str = None
        self.accountNumber: str = None
        self.accountName: str = None
        self.code: str = None
        self.matchedQuantity: int = None
        self.buyPrice: float = None
        self.sellPrice: float = None
        self.realizedPl: float = None
        self.commission: str = None
        self.netProfitLoss: str = None
        self.userId: str = None
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.closeDate = data[:8].decode().strip()
        instance.accountNumber = data[8:18].decode().strip()
        instance.accountName = data[18:118].decode().strip()
        instance.code = data[118:148].decode().strip()
        instance.matchedQuantity = int(data[148:155].decode().strip() or '0')
        instance.buyPrice = float(data[155:170].decode().strip() or '0')
        instance.sellPrice = float(data[170:185].decode().strip() or '0')
        instance.realizedPl = float(data[185:206].decode().strip() or '0')
        instance.commission = data[206:221].decode().strip()
        instance.netProfitLoss = float(data[221:242].decode().strip() or '0')
        instance.userId = data[242:257].decode().strip()
        return instance
