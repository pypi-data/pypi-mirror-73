from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class RightOtherReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'lastStockCode', 'lastBaseDate', 'lastRightType', 'fetchCount'

    def __init__(self):
        super(RightOtherReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.lastStockCode: str = None
        self.lastBaseDate: str = None
        self.lastRightType: str = None
        self.fetchCount: int = None


class RightOtherRes(Base):
    __slots__ = 'stockCode', 'rightName', 'baseDate', 'receiptQuantity', 'receiptDate', \
                'dividendAmount', 'dividendDate'

    def __init__(self):
        super(RightOtherRes, self).__init__()
        self.stockCode: str = None
        self.rightName: str = None
        self.baseDate: str = None
        self.receiptQuantity: int = None
        self.receiptDate: str = None
        self.dividendAmount: float = None
        self.dividendDate: str = None
