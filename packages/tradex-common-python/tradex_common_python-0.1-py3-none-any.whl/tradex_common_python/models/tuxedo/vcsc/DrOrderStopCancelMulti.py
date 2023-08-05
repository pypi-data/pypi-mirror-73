from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from typing import List


class DrOrderStopCancelMultiReq(Request):
    __slots__ = 'orderList'

    def __init__(self):
        super(DrOrderStopCancelMultiReq, self).__init__()
        self.orderList: List[DrOrderStopCancelMultiItem] = []


class DrOrderStopCancelMultiItem(Base):
    __slots__ = 'createdDate', 'sequenceNumber', 'accountNumber', 'password'

    def __init__(self):
        super(DrOrderStopCancelMultiItem, self).__init__()
        self.createdDate: str = ''
        self.sequenceNumber: str = ''
        self.accountNumber: str = ''
        self.password: str = ''

    def to_string(self) -> str:
        data = self.createdDate[:8].ljust(8, ' ')           # b_n01
        data += self.sequenceNumber[:15].ljust(15, ' ')     # b_n02
        data += self.accountNumber[:10].ljust(10, ' ')      # b_n03
        data += self.password[:64].ljust(64, ' ')           # b_n04
        return data


class DrOrderStopCancelMultiRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(DrOrderStopCancelMultiRes, self).__init__()
        self.message: str = None
