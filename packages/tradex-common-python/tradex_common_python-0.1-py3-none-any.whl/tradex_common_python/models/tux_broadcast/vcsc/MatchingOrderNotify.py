from tradex_common_python.models.Base import Base
from tradex_common_python.models.tux_broadcast.vcsc.SocketClusterNotify import SocketClusterNotify


class MatchingOrderNotify(Base):
    __slots__ = 'orderNumber', 'originalOrderNumber', 'username', 'accountNumber', 'subNumber', \
                'orderPrice', 'orderQuantity', 'matchPrice', 'matchQuantity', 'totalMatchQuantity', \
                'unmatchQuantity', 'code', 'sellBuyType', 'marketType', 'time', 'execNo', 'domain'

    def __init__(self):
        super(MatchingOrderNotify, self).__init__()
        self.orderNumber: str = None
        self.originalOrderNumber: str = None
        self.username: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.orderPrice: float = None
        self.orderQuantity: int = None
        self.matchPrice: float = None
        self.matchQuantity: int = None
        self.totalMatchQuantity: int = None
        self.unmatchQuantity: int = None
        self.code: str = None
        self.sellBuyType: str = None
        self.marketType: str = None
        self.time: str = None
        self.execNo: str = None
        self.domain: str = None

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
