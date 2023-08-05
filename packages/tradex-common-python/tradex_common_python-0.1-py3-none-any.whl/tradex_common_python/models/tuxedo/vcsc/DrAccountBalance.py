from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrAccountBalanceReq(Request):
    __slots__ = 'fromDate', 'toDate', 'accountNumber', 'lastNextKey', 'fetchCount', 'password'

    def __init__(self):
        super(DrAccountBalanceReq, self).__init__()
        self.accountNumber: str = ''
        self.fromDate: str = ''
        self.toDate: str = ''
        self.lastNextKey: str = ''
        self.password: str = ''
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


class DrAccountBalanceRes(Base):
    __slots__ = 'date', 'previousCashBalance', 'depositBalance', 'withdrawableBalance', 'cashBalance', \
                'previousSubstituteBalance', 'depositSubstituteBalance', 'withdrawableSubstituteBalance', \
                'substituteBalance', 'marginRequirement', 'nextKey', 'accountNumber', 'accountName'

    def __init__(self):
        super(DrAccountBalanceRes, self).__init__()
        self.accountNumber: str = None
        self.accountName: str = None
        self.date: str = None
        self.previousCashBalance: float = None
        self.depositBalance: float = None
        self.withdrawableBalance: float = None
        self.cashBalance: float = None
        self.previousSubstituteBalance: float = None
        self.depositSubstituteBalance: float = None
        self.withdrawableSubstituteBalance: float = None
        self.substituteBalance: float = None
        self.marginRequirement: float = None
        self.nextKey: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.date = data[:8].decode().strip()
        instance.accountNumber = data[8:18].decode().strip()
        instance.accountName = data[18:118].decode().strip()
        instance.previousCashBalance = float(data[118:136].decode().strip() or '0')
        instance.depositBalance = float(data[136:154].decode().strip() or '0')
        instance.withdrawableBalance = float(data[154:172].decode().strip() or '0')
        instance.cashBalance = float(data[172:190].decode().strip() or '0')
        instance.previousSubstituteBalance = float(data[190:208].decode().strip() or '0')
        instance.depositSubstituteBalance = float(data[208:226].decode().strip() or '0')
        instance.withdrawableSubstituteBalance = float(data[226:244].decode().strip() or '0')
        instance.substituteBalance = float(data[244:262].decode().strip() or '0')
        instance.marginRequirement = float(data[262:280].decode().strip() or '0')
        return instance