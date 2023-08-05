from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from typing import List


class DrOrderAdvCancelMultiReq(Request):
    __slots__ = 'orderList'

    def __init__(self):
        super(DrOrderAdvCancelMultiReq, self).__init__()
        self.orderList: List[DrOrderAdvCancelMultiItem] = []


class DrOrderAdvCancelMultiItem(Base):
    __slots__ = 'accountNumber', 'password', 'tradingDate', 'marketSession', 'orderNumber', 'code'

    def __init__(self):
        super(DrOrderAdvCancelMultiItem, self).__init__()
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


class DrOrderAdvCancelMultiRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(DrOrderAdvCancelMultiRes, self).__init__()
        self.message: str = None
