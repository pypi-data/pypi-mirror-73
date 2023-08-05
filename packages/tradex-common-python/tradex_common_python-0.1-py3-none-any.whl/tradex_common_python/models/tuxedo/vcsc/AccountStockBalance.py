from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountStockBalanceReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'lastStockCode', 'fetchCount', 'bankName'

    def __init__(self):
        super(AccountStockBalanceReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.lastStockCode: str = None
        self.fetchCount: int = None
        self.bankName: str = None


class AccountStockBalanceRes(Base):
    __slots__ = 'stockCode', 'balanceQuantity', 'buyAmount', 'evaluationAmount', 'pendingBuyQuantity', \
                'pendingSellQuantity', 'orderAvailableQuantity', 'unsellableQuantity', 'blockQuantity', \
                'deliveryPendingQuantity', 'totalPendingQuantity'

    def __init__(self):
        super(AccountStockBalanceRes, self).__init__()
        self.stockCode: str = None
        self.balanceQuantity: int = None
        self.buyAmount: float = None
        self.evaluationAmount: float = None
        self.pendingBuyQuantity: int = None
        self.pendingSellQuantity: int = None
        self.orderAvailableQuantity: int = None
        self.unsellableQuantity: int = None
        self.blockQuantity: int = None
        self.deliveryPendingQuantity: int = None
        self.totalPendingQuantity: int = None
