from tradex_common_python.models.Base import Base
from tradex_common_python.models.tux_broadcast.vcsc.SocketClusterNotify import SocketClusterNotify
from datetime import datetime, timedelta


def convert24(time_str):
    hours = int(time_str[:2])
    if hours < 7:
        return str(int(time_str[:2]) + 12) + time_str[2:6]
    return time_str


class DrMatchingOrderNotify(Base):
    __slots__ = (
        'orderNumber', 'execNo', 'originalOrderNumber', 'orderPrice', 'orderQuantity',
        'modifyCancelQuantity', 'matchPrice', 'matchQuantity', 'totalMatchQuantity', 'marketType',
        'sellBuyType', 'accountNumber', 'username', 'time', 'code', 'codeName', 'unmatchQuantity',
        'subNumber'
    )

    def __init__(self):
        super(DrMatchingOrderNotify, self).__init__()
        self.orderNumber: str = None
        self.execNo: str = None
        self.originalOrderNumber: str = None
        self.orderPrice: float = None
        self.orderQuantity: int = None
        self.modifyCancelQuantity: int = None
        self.matchPrice: float = None
        self.matchQuantity: int = None
        self.totalMatchQuantity: int = None
        self.marketType: str = None
        self.sellBuyType: str = None
        self.accountNumber: str = None
        self.username: str = None
        self.time: str = None
        self.code: str = None
        self.codeName: str = None
        self.unmatchQuantity: int = None  # addition field
        self.subNumber: str = ""

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.orderNumber: str = data[:10].decode().strip()
        instance.execNo = data[10:30].decode().strip()
        instance.originalOrderNumber = data[30:40].decode().strip()
        instance.orderPrice = data[40:50].decode().strip()
        instance.orderQuantity = int(data[50:60].decode().strip())
        instance.modifyCancelQuantity = int(data[60:70].decode().strip())
        instance.matchPrice = float(data[70:80].decode().strip())
        instance.matchQuantity = int(data[80:90].decode().strip())
        instance.totalMatchQuantity = int(data[90:100].decode().strip())
        instance.marketType = data[100:101].decode().strip()
        instance.sellBuyType = data[101:102].decode().strip()
        instance.accountNumber = data[102:112].decode().strip()
        instance.username = data[112:127].decode().strip()
        match_order_time = data[127:135].decode().strip().replace(":", "").rjust(6, "0")
        match_order_time = convert24(match_order_time)
        match_order_date_time = datetime.strptime(datetime.now().strftime('%Y%m%d') + match_order_time, "%Y%m%d%H%M%S")
        match_order_date_time = match_order_date_time - timedelta(hours=7)
        instance.time = datetime.strftime(match_order_date_time, "%H%M%S")
        instance.code = data[135:155].decode().strip()
        instance.codeName = data[155:185].decode().strip()
        instance.unmatchQuantity = instance.orderQuantity - instance.totalMatchQuantity
        return instance

    def to_notify_message(self):
        notify = SocketClusterNotify()
        channel = 'domain.notify.account.' + self.accountNumber + self.subNumber
        notify.method = 'SOCKET_CLUSTER'
        notify.template = {
            'template_1': {
                'method': 'MATCH_ORDER',
                'payload': self.to_dict()
            }
        }
        notify.configuration = "{\"channel\":\""+channel+"\"}"
        return notify
