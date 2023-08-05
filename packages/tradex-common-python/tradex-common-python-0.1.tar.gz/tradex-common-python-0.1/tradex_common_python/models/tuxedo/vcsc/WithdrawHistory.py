from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class WithdrawHistoryReq(Request):
    __slots__ = 'status', 'accountNumber', 'subNumber', 'fromDate', 'toDate', 'lastTransactionDate', \
                'lastSequenceNumber', 'fetchCount'

    def __init__(self):
        super(WithdrawHistoryReq, self).__init__()
        self.status: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.lastTransactionDate: str = None
        self.lastSequenceNumber: int = None
        self.fetchCount: int = None


class WithdrawHistoryRes(Base):
    __slots__ = 'transactionDate', 'transactionType', 'bank', 'note', 'amount', 'transactionSequenceNumber', \
                'approver', 'approvalDate', 'sequenceNumber', 'isCancel', 'bankAccount', 'bankCode', 'bankName', \
                'transactionCode'

    def __init__(self):
        super(WithdrawHistoryRes, self).__init__()
        self.transactionDate: str = None
        self.transactionType: str = None
        self.transactionCode: str = None
        self.bank: str = None
        self.note: str = None
        self.amount: float = None
        self.transactionSequenceNumber: int = None
        self.approver: str = None
        self.approvalDate: str = None
        self.sequenceNumber: int = None
        self.isCancel: bool = None
        self.bankAccount: str = None
        self.bankCode: str = None
        self.bankName: str = None
