from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class RightAvailableReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'rightType', 'fetchCount', 'lastBaseDate', \
                'lastStockCode', 'lastSequenceNumber'

    def __init__(self):
        super(RightAvailableReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.rightType: str = None
        self.fetchCount: int = None
        self.lastBaseDate: str = None
        self.lastStockCode: str = None
        self.lastSequenceNumber: str = None


class RightAvailableRes(Base):
    __slots__ = 'stockCode', 'stockName', 'sequenceNumber', 'baseDate', 'rightStatus', 'startDate', 'endDate', \
                'issuePrice', 'availableQuantity', 'note'

    def __init__(self):
        super(RightAvailableRes, self).__init__()
        self.stockCode: str = None
        self.stockName: str = None
        self.sequenceNumber: int = None
        self.baseDate: str = None
        self.rightStatus: str = None
        self.startDate: str = None
        self.endDate: str = None
        self.issuePrice: float = None
        self.availableQuantity: int = None
        self.note: str = None
