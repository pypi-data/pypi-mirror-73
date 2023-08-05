from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrStopOrderHistoryReq(Request):
    __slots__ = 'accountNumber', 'password', 'fromDate', 'toDate', 'contactCode', 'sellBuyType', 'orderType', \
                'validity', 'registered', 'sent', 'branchCode', 'agencyCode', 'lastNextKey', 'fetchCount', 'isSent', \
                'isRegistered'

    def __init__(self):
        super(DrStopOrderHistoryReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.fromDate: str = ''
        self.toDate: str = ''
        self.contactCode: str = ''
        self.sellBuyType: str = ''
        self.orderType: str = ''
        self.validity: str = ''
        self.registered: str = ''
        self.sent: str = ''
        self.branchCode: str = ''
        self.agencyCode: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = None
        self.isSent: bool = None              # addition field
        self.isRegistered: bool = None        # addition field

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        data += self.fromDate[:8].ljust(8, ' ')             # b_n03
        data += self.toDate[:8].ljust(8, ' ')               # b_n04
        data += self.contactCode[:30].ljust(30, ' ')        # b_n05
        data += self.sellBuyType[:1].ljust(1, ' ')          # b_n06
        data += self.orderType[:1].ljust(1, ' ')            # b_n07
        data += self.validity[:1].ljust(1, ' ')             # b_n08
        data += self.registered[:1].ljust(1, ' ')           # b_n09
        data += self.sent[:1].ljust(1, ' ')                 # b_n10
        data += self.branchCode[:3].ljust(3, ' ')           # b_n11
        data += self.agencyCode[:2].ljust(2, ' ')           # b_n12
        last_next_key = ''
        #  sprintf(ts_grdhdr,"%-s%-3s%-4s%-70s",(flags == QRY ? "0" : "2")," ","0",inext);
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')                 # b_n13
        return data


class DrStopOrderHistoryRes(Base):
    __slots__ = 'date', 'sequenceNumber', 'originalOrderNumber', 'accountNumber', 'accountName', 'code', \
                'codeName', 'sellBuyType', 'orderType', 'status', 'orderQuantity', 'orderPrice', 'bandPrice', \
                'fromDate', 'toDate', 'mdmType', 'username', 'registered', 'registeredDate', 'cancelUsername', \
                'cancelDateTime', 'sendYn', 'tradingDate', 'orderNumber', 'errorCode', 'errorMessage', 'ip', \
                'operator', 'operatingTime', 'nextKey', 'stopPrice', 'isSent', 'isRegistered'

    def __init__(self):
        super(DrStopOrderHistoryRes, self).__init__()
        self.date: str = None
        self.sequenceNumber: str = None
        self.originalOrderNumber: str = None
        self.accountNumber: str = None
        self.accountName: str = None
        self.code: str = None
        self.codeName: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.status: str = None
        self.orderQuantity: int = None
        self.orderPrice: float = None
        self.bandPrice: float = None
        self.fromDate: str = None
        self.toDate: str = None
        self.mdmType: str = None
        self.username: str = None
        self.registered: str = None
        self.registeredDate: str = None
        self.cancelUsername: str = None
        self.cancelDateTime: str = None
        self.sendYn: str = None
        self.tradingDate: str = None
        self.orderNumber: str = None
        self.errorCode: str = None
        self.errorMessage: str = None
        self.ip: str = None
        self.operator: str = None
        self.operatingTime: str = None
        self.nextKey: str = None
        self.stopPrice: float = None  # addition field
        self.isSent: bool = None  # addition field
        self.isRegistered: bool = None  # addition field

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.date: str = data[:8].decode().strip()
        instance.sequenceNumber = data[8:23].decode().strip()
        instance.originalOrderNumber = data[23:38].decode().strip()
        instance.accountNumber = data[38:48].decode().strip()
        instance.accountName = data[48:148].decode().strip()
        instance.code = data[148:178].decode().strip()
        instance.codeName = data[178:278].decode().strip()
        instance.sellBuyType = data[278:279].decode().strip()
        instance.orderType = data[279:280].decode().strip()
        instance.status = data[280:281].decode().strip()
        instance.orderQuantity = int(data[281:288].decode().strip() or '0')
        instance.orderPrice = float(data[288:303].decode().strip() or '0')
        instance.bandPrice = float(data[303:318].decode().strip() or '0')
        instance.fromDate = data[318:326].decode().strip()
        instance.toDate = data[326:334].decode().strip()
        instance.mdmType = data[336:336].decode().strip()
        instance.username = data[336:351].decode().strip()
        instance.registered = data[351:352].decode().strip()
        instance.registeredDate = data[352:366].decode().strip()
        instance.cancelUsername = data[366:381].decode().strip()
        instance.cancelDateTime = data[381:395].decode().strip()
        instance.sendYn = data[395:396].decode().strip()
        instance.tradingDate = data[396:404].decode().strip()
        instance.orderNumber = data[404:411].decode().strip()
        instance.errorCode = data[411:431].decode().strip()
        instance.errorMessage = data[431:631].decode().strip()
        instance.ip = data[631:645].decode().strip()
        instance.operator = data[645:661].decode().strip()
        instance.operatingTime = data[661:675].decode().strip()
        return instance
