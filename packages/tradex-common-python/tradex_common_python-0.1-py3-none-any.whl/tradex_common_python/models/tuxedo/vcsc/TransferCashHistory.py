from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class TransferCashHistoryReq(Request):
    __slots__ = 'status', 'accountNumber', 'subNumber', 'fromDate', 'toDate', 'lastTransactionDate', \
                'lastTransferSequenceNumber', 'fetchCount', 'type'

    def __init__(self):
        super(TransferCashHistoryReq, self).__init__()
        self.status: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.lastTransactionDate: str = None
        self.lastTransferSequenceNumber: str = None
        self.type: str = None
        self.fetchCount: int = None


class TransferCashHistoryRes(Base):
    __slots__ = 'transactionDate', 'receivedAccountNumber', 'receivedSubNumber', 'receivedAccountName', \
                'amount', 'accountNumber', 'subNumber', 'note', 'sequenceNumber', 'sendSequenceNumber', \
                'receiveSequenceNumber', 'isCancel', 'transferSequenceNumber'

    def __init__(self):
        super(TransferCashHistoryRes, self).__init__()
        self.transactionDate: str = None
        self.receivedAccountNumber: str = None
        self.receivedSubNumber: str = None
        self.receivedAccountName: str = None
        self.amount: float = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.note: str = None
        self.sequenceNumber: int = None
        self.sendSequenceNumber: int = None
        self.receiveSequenceNumber: int = None
        self.transferSequenceNumber: int = None
        self.isCancel: bool = None
