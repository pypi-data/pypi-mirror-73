from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class TransferStockReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'receivedAccountNumber', 'receivedSubNumber', 'stockCode', \
                'quantity', 'limitedQuantity', 'note'

    def __init__(self):
        super(TransferStockReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.receivedAccountNumber: str = None
        self.receivedSubNumber: str = None
        self.stockCode: str = None
        self.quantity: int = None
        self.limitedQuantity: int = None
        self.note: str = None


class TransferStockRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(TransferStockRes, self).__init__()
        self.message: str = None
