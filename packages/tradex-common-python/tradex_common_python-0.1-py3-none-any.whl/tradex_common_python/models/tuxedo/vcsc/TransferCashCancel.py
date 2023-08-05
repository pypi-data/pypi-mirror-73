from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class TransferCashCancelReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'sequenceNumber', 'sendSequenceNumber', \
                'receivedAccountNumber', 'receivedSubNumber', 'receiveSequenceNumber', 'amount', 'note'

    def __init__(self):
        super(TransferCashCancelReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.sequenceNumber: str = None
        self.sendSequenceNumber: str = None
        self.receivedAccountNumber: str = None
        self.receivedSubNumber: str = None
        self.receiveSequenceNumber: str = None
        self.amount: float = None
        self.note: str = None


class TransferCashCancelRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(TransferCashCancelRes, self).__init__()
        self.message: str = None
