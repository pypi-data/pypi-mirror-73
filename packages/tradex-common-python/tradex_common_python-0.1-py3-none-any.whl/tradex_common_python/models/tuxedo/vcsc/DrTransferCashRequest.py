from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrTransferCashRequestReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'receivedSubNumber', 'amount', 'note', 'bankCode'

    def __init__(self):
        super(DrTransferCashRequestReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.receivedSubNumber: str = None
        self.amount: str = None
        self.note: str = None
        self.bankCode: str = None


class DrTransferCashRequestRes(Base):
    __slots__ = 'transactionDate', 'outSequenceNumber', 'outPreviousCashBalance', 'outCashBalance', \
                'inSequenceNumber', 'inPreviousCashBalance', 'inCashBalance'

    def __init__(self):
        super(DrTransferCashRequestRes, self).__init__()
        self.transactionDate: str = None
        self.outSequenceNumber: str = None
        self.outPreviousCashBalance: float = None
        self.outCashBalance: float = None
        self.inSequenceNumber: str = None
        self.inPreviousCashBalance: float = None
        self.inCashBalance: float = None
