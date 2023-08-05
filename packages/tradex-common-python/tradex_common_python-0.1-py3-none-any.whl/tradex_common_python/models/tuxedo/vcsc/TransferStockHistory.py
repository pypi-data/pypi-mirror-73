from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class TransferStockHistoryReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'fromDate', 'toDate', 'branchCode', 'lastTransactionDate', \
                'lastReceivedAccountNumber', 'lastSequenceNumber', 'fetchCount'

    def __init__(self):
        super(TransferStockHistoryReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.branchCode: str = None
        self.lastTransactionDate: str = None
        self.lastReceivedAccountNumber: str = None
        self.lastSequenceNumber: int = None
        self.fetchCount: int = None


class TransferStockHistoryRes(Base):
    __slots__ = 'transactionDate', 'sequenceNumber', 'accountNumber', 'subNumber', 'receivedAccountNumber', \
                'receivedSubNumber', 'stockCode', 'quantity', 'limitedQuantity', 'note'

    def __init__(self):
        super(TransferStockHistoryRes, self).__init__()
        self.transactionDate: str = None
        self.sequenceNumber: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.receivedAccountNumber: str = None
        self.receivedSubNumber: str = None
        self.stockCode: str = None
        self.quantity: int = None
        self.limitedQuantity: int = None
        self.note: str = None
