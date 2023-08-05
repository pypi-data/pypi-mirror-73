from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from tradex_common_python.models.tuxedo.vcsc.DrOrderStopCancelMulti import DrOrderStopCancelMultiReq, \
    DrOrderStopCancelMultiItem


class DrOrderStopCancelReq(Request):
    __slots__ = 'createdDate', 'sequenceNumber', 'accountNumber', 'password'

    def __init__(self):
        super(DrOrderStopCancelReq, self).__init__()
        self.createdDate: str = ''
        self.sequenceNumber: str = ''
        self.accountNumber: str = ''
        self.password: str = ''

    def to_string(self) -> str:
        data = self.createdDate[:8].ljust(8, ' ')                  # b_n01
        data += self.sequenceNumber[:15].ljust(15, ' ')     # b_n02
        data += self.accountNumber[:10].ljust(10, ' ')      # b_n03
        data += self.password[:64].ljust(64, ' ')           # b_n04
        return data

    @classmethod
    def from_request_multi(cls, request: DrOrderStopCancelMultiReq, request_item: DrOrderStopCancelMultiItem):
        instance = cls()
        instance.headers = request.headers
        instance.sourceIp = request.sourceIp
        instance.deviceType = request.deviceType
        instance.createdDate = request_item.createdDate
        instance.sequenceNumber = request_item.sequenceNumber
        instance.accountNumber = request_item.accountNumber
        instance.password = request_item.password
        return instance


class DrOrderStopCancelRes(Base):
    __slots__ = 'dummy'

    def __init__(self):
        super(DrOrderStopCancelRes, self).__init__()
        self.dummy: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.dummy = data[:1].decode().strip()
        return instance
