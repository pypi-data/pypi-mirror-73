from typing import Dict, List

from tradex_common_python.models.Base import Base, create_key_map_from_array
from tradex_common_python.models.tux_broadcast.vcsc.SocketClusterNotify import SocketClusterNotify

user_login_notify_key_map: Dict = None


class Account(Base):
    __slots__ = 'accountNumber', 'subNumber'

    def __init__(self):
        super(Account, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None


class UserLoginNotification(Base):
    __slots__ = 'accounts', 'mediaType', 'serverIp', 'clientIp', 'username', 'isFromTradex'

    def __init__(self):
        super(UserLoginNotification, self).__init__()
        self.accounts: List[Account] = []
        self.username: str = None
        self.mediaType: str = None
        self.serverIp: str = None
        self.clientIp: str = None
        self.isFromTradex: bool = False

    def key_mapping(self) -> Dict[str, str]:
        global user_login_notify_key_map
        if user_login_notify_key_map is None:
            user_login_notify_key_map = create_key_map_from_array(self.__slots__)
        return user_login_notify_key_map

    def to_notify_message(self):
        notify = SocketClusterNotify()
        channel = 'domain.notify.username.' + self.username
        notify.method = 'SOCKET_CLUSTER'
        notify.template = {
            'template_1': {
                'method': 'USER_LOGIN',
                'payload': self.to_dict()
            }
        }
        notify.configuration = "{\"channel\":\""+channel+"\"}"
        return notify
