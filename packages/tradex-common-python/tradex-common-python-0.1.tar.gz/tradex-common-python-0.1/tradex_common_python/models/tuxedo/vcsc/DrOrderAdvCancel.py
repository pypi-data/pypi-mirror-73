from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from tradex_common_python.models.tuxedo.vcsc.DrOrderAdvCancelMulti import DrOrderAdvCancelMultiReq, DrOrderAdvCancelMultiItem


class DrOrderAdvCancelReq(Request):
    __slots__ = 'accountNumber', 'password', 'tradingDate', 'marketSession', 'orderNumber', 'code'

    def __init__(self):
        super(DrOrderAdvCancelReq, self).__init__()
        self.accountNumber: str = ''
        self.password: str = ''
        self.tradingDate: str = ''
        self.marketSession: str = ''
        self.orderNumber: str = ''
        self.code: str = ''

    def to_string(self) -> str:
        data = self.accountNumber[:10].ljust(10, ' ')           # b_n01
        data += self.password[:64].ljust(64, ' ')               # b_n02
        data += self.tradingDate[:8].ljust(8, ' ')              # b_n03
        data += self.marketSession[:1].ljust(1, ' ')            # b_n04
        data += self.orderNumber[:15].ljust(15, ' ')            # b_n05
        data += self.code[:30].ljust(30, ' ')                   # b_n06
        return data

    @classmethod
    def from_request_multi(cls, request: DrOrderAdvCancelMultiReq, request_item: DrOrderAdvCancelMultiItem):
        instance = cls()
        instance.headers = request.headers
        instance.sourceIp = request.sourceIp
        instance.deviceType = request.deviceType
        instance.accountNumber = request_item.accountNumber
        instance.password = request_item.password
        instance.tradingDate = request_item.tradingDate
        instance.marketSession = request_item.marketSession
        instance.orderNumber = request_item.orderNumber
        instance.code = request_item.code
        return instance


class DrOrderAdvCancelRes(Base):
    __slots__ = 'dummy'

    def __init__(self):
        super(DrOrderAdvCancelRes, self).__init__()
        self.dummy: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.dummy = data[:1].decode().strip()
        return instance
