from typing import List
from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class OrderHistoryByNoReq(Request):
    __slots__ = 'orderNumbers', 'accountNo', 'includeStatus'

    def __init__(self):
        super(Request, self).__init__()
        self.orderNumbers: List[str] = None
        self.accountNo: str = None
        self.includeStatus: bool = True

######
# RECEIPT = '0'
# SEND = '1'
# ORDER_CONFIRM = '2'
# RECEIPT_CONFIRM = '3'
# FULL_FILLED = '4'
# PARTIAL_FILLED = '5'
# REJECT = 'X'
#######


class OrderStatus:
    def __init__(self):
        self.UNKNOWN: int = 0
        self.RECEIPT: int = 1
        self.SEND: int = 2
        self.ORDER_CONFIRM: int = 3
        self.RECEIPT_CONFIRM: int = 4
        self.FULL_FILLED: int = 5
        self.PARTIAL_FILLED: int = 6
        self.REJECT: int = 7


ORDER_STATUSES = OrderStatus()
ORDER_STATUSES_MAP = {
    '0': ORDER_STATUSES.RECEIPT,
    '1': ORDER_STATUSES.SEND,
    '2': ORDER_STATUSES.ORDER_CONFIRM,
    '3': ORDER_STATUSES.RECEIPT_CONFIRM,
    '4': ORDER_STATUSES.FULL_FILLED,
    '5': ORDER_STATUSES.PARTIAL_FILLED,
    'X': ORDER_STATUSES.REJECT,
}


class OrderHistoryByNoRes(Base):
    __slots__ = 'odNo', 'mthQty', 'mthPx', 'st'

    def __init__(self):
        super(Base, self).__init__()
        self.odNo: str = None
        self.mthQty: int = None
        self.mthPx: float = None
        self.st: int = None

    def set_status(self, value: str):
        if value in ORDER_STATUSES_MAP:
            self.st = ORDER_STATUSES_MAP[value]
        else:
            self.st = ORDER_STATUSES.UNKNOWN
