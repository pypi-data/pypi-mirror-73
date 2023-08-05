from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class RightDetailReq(Request):
    __slots__ = 'stockCode', 'accountNumber', 'subNumber', 'baseDate', 'rightType', 'sequenceNumber', \
                'bankCode', 'bankAccount', 'bankName'

    def __init__(self):
        super(RightDetailReq, self).__init__()
        self.stockCode: str = None
        self.accountNumber: str = None
        self.subNumber: str = None
        self.baseDate: str = None
        self.rightType: str = None
        self.sequenceNumber: int = None
        self.bankCode: str = None
        self.bankAccount: str = None
        self.bankName: str = None


class RightDetailRes(Base):
    __slots__ = 'issuePrice', 'standardQuantity', 'availableQuantity', 'quantity', 'amount', 'availableAmount', \
                'tradeNumber', 'bankApproveWaitingQuantity', 'bankCancelWaitingQuantity', 'approveWaitingQuantity', \
                'startDate', 'endDate', 'processStatusCode', 'processStatusName', 'rightType'

    def __init__(self):
        super(RightDetailRes, self).__init__()
        self.issuePrice: float = None
        self.standardQuantity: int = None
        self.availableQuantity: int = None
        self.quantity: str = None
        self.amount: float = None
        self.availableAmount: float = None
        self.tradeNumber: str = None
        self.bankApproveWaitingQuantity: int = None
        self.bankCancelWaitingQuantity: int = None
        self.approveWaitingQuantity: int = None
        self.startDate: float = None
        self.endDate: float = None
        self.processStatusCode: int = None
        self.processStatusName: float = None
        self.rightType: float = None
