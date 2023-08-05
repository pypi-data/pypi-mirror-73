from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrImHistoryReq(Request):
    __slots__ = 'accountNumber', 'type', 'fromDate', 'toDate', 'lastTransactionDate', 'lastSequenceNumber', 'fetchCount'

    def __init__(self):
        super(DrImHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.type: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.lastTransactionDate: str = None
        self.lastSequenceNumber: str = None
        self.fetchCount: int = None


class DrImHistoryRes(Base):
    __slots__ = 'sequenceNumber', 'transactionDate', 'transactionType', 'amount', 'receivedAmount', \
                'feeAmount', 'note', 'isCancel', 'sourceBank', 'destBank', 'bankStatus', 'bosStatus', 'vsdStatus'

    def __init__(self):
        super(DrImHistoryRes, self).__init__()
        self.sequenceNumber: str = None
        self.transactionDate: str = None
        self.transactionType: str = None
        self.amount: float = None
        self.receivedAmount: float = None
        self.feeAmount: float = None
        self.note: str = None
        self.isCancel: bool = None
        self.sourceBank: str = None
        self.destBank: str = None
        self.bankStatus: str = None
        self.bosStatus: str = None
        self.vsdStatus: str = None
