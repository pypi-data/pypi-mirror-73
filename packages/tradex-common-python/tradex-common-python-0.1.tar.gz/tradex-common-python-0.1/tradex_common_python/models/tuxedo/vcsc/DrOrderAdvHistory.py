from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrOrderAdvHistoryReq(Request):
    __slots__ = 'accountNumber', 'password', 'advanceOrderType', 'fromDate', 'toDate', 'registerType', 'orderSend', \
                'matchedStatus', 'validity', 'branchCode', 'agencyCode', 'contractCode', 'sellBuyType', \
                'rollOverType', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrOrderAdvHistoryReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.advanceOrderType: str = ''
        self.fromDate: str = ''
        self.toDate: str = ''
        self.registerType: str = ''
        self.orderSend: str = ''
        self.matchedStatus: str = ''
        self.validity: str = ''
        self.branchCode: str = ''
        self.agencyCode: str = ''
        self.contractCode: str = ''
        self.sellBuyType: str = ''
        self.rollOverType: str = ''
        self.lastNextKey: str = ''
        self.fetchCount: int = 20

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')       # b_n01
        data += self.password[:64].ljust(64, ' ')           # b_n02
        data += self.advanceOrderType[:64].ljust(1, ' ')              # b_n03
        data += self.fromDate[:8].ljust(8, ' ')             # b_n04
        data += self.toDate[:8].ljust(8, ' ')               # b_n05
        data += self.registerType[:1].ljust(1, ' ')         # b_n06
        data += self.orderSend[:1].ljust(1, ' ')            # b_n07
        data += self.matchedStatus[:1].ljust(1, ' ')            # b_n08
        data += self.validity[:1].ljust(1, ' ')             # b_n09
        data += self.branchCode[:3].ljust(3, ' ')           # b_n10
        data += self.agencyCode[:2].ljust(2, ' ')           # b_n11
        data += self.contractCode[:30].ljust(30, ' ')       # b_n12
        data += self.sellBuyType[:1].ljust(1, ' ')          # b_n13
        data += self.rollOverType[:1].ljust(1, ' ')         # b_n14
        last_next_key = ''
        #  sprintf(ts_grdhdr,"%-s%-3s%-4s%-70s",(flags == QRY ? "0" : "2")," ","0",inext);
        if self.lastNextKey is not None and len(self.lastNextKey) > 0:
            last_next_key += '2   0   '
            last_next_key += self.lastNextKey[:70].ljust(70, ' ')
        data += last_next_key.ljust(78, ' ')            # b_n15
        return data


class DrOrderAdvHistoryRes(Base):
    __slots__ = 'date', 'advanceOrderType', 'fromDate', 'toDate', 'sequenceNumber', 'marketSession', 'accountNumber', \
                'accountName', 'code', 'codeName', 'sellBuyType', 'orderType', 'validity', 'orderQuantity', \
                'rollOverQuantity', 'orderPrice', 'mdmType', 'username', 'cancelUsername', 'registerYn', 'sendYn', \
                'orderSendStatus', 'matchedStatus', 'matchedQuantity', 'averageMatchedPrice', 'unmatchedQuantity', \
                'modifyCancelQuantity', 'cancelModifyTime', 'cancelModifyId', 'validStatus', 'orderNumber', \
                'errorCode', 'errorMessage', 'registeredDate', 'cancelDateTime', 'ip', 'operator', 'operatingTime', \
                'nextKey', 'isValid', 'isSent',  'isRegistered'

    def __init__(self):
        super(DrOrderAdvHistoryRes, self).__init__()
        self.date: str = None
        self.advanceOrderType: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.sequenceNumber: str = None
        self.marketSession: str = None
        self.accountNumber: str = None
        self.accountName: str = None
        self.code: str = None
        self.codeName: str = None
        self.sellBuyType: str = None
        self.orderType: str = None
        self.validity: str = None
        self.orderQuantity: int = None
        self.rollOverQuantity: int = None
        self.orderPrice: float = None
        self.mdmType: str = None
        self.username: str = None
        self.cancelUsername: str = None
        self.registerYn: str = None
        self.sendYn: str = None
        self.orderSendStatus: str = None
        self.matchedStatus: str = None
        self.matchedQuantity: int = None
        self.averageMatchedPrice: float = None
        self.unmatchedQuantity: int = None
        self.modifyCancelQuantity: int = None
        self.cancelModifyTime: str = None
        self.cancelModifyId: str = None
        self.validStatus: str = None
        self.orderNumber: str = None
        self.errorCode: str = None
        self.errorMessage: str = None
        self.registeredDate: str = None
        self.cancelDateTime: str = None
        self.ip: str = None
        self.operator: str = None
        self.operatingTime: str = None
        self.nextKey: str = None
        self.isValid: bool = None  # addition field
        self.isSent: bool = None              # addition field
        self.isRegistered: bool = None        # addition field

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.date: str = data[:8].decode().strip()
        instance.advanceOrderType = data[8:9].decode().strip()
        instance.fromDate = data[9:17].decode().strip()
        instance.toDate = data[17:25].decode().strip()
        instance.sequenceNumber = data[25:40].decode().strip()
        instance.marketSession = data[40:41].decode().strip()
        instance.accountNumber = data[41:51].decode().strip()
        instance.accountName = data[51:151].decode().strip()
        instance.code = data[151:181].decode().strip()
        instance.codeName = data[181:281].decode().strip()
        instance.sellBuyType = data[281:282].decode().strip()
        instance.orderType = data[282:283].decode().strip()
        instance.validity = data[283:284].decode().strip()
        instance.orderQuantity = data[284:291].decode().strip()
        instance.rollOverQuantity = data[291:298].decode().strip()
        instance.orderPrice = float(data[298:313].decode().strip() or '0')
        instance.mdmType = data[313:315].decode().strip()
        instance.username = data[315:330].decode().strip()
        instance.cancelUsername = data[330:345].decode().strip()
        instance.registerYn = data[345:346].decode().strip()
        instance.sendYn = data[346:347].decode().strip()
        instance.orderSendStatus = data[347:348].decode().strip()
        instance.matchedStatus = data[348:349].decode().strip()
        instance.matchedQuantity = data[349:356].decode().strip()
        instance.averageMatchedPrice = data[356:371].decode().strip()
        instance.unmatchedQuantity = data[371:378].decode().strip()
        instance.modifyCancelQuantity = data[378:385].decode().strip()
        instance.cancelModifyTime = data[385:399].decode().strip()
        instance.cancelModifyId = data[399:414].decode().strip()
        instance.validStatus = data[414:415].decode().strip()
        instance.orderNumber = data[415:422].decode().strip()
        instance.errorCode = data[422:442].decode().strip()
        instance.errorMessage = data[442:642].decode().strip()
        instance.registeredDate = data[642:656].decode().strip()
        instance.cancelDateTime = data[656:670].decode().strip()
        instance.ip = data[670:685].decode().strip()
        instance.operator = data[685:700].decode().strip()
        instance.operatingTime = data[700:714].decode().strip()
        return instance
