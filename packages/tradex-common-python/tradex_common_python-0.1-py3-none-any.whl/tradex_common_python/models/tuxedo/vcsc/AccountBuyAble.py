from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountBuyAbleReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'bankCode', 'stockCode', 'securitiesType', \
                'marketType', 'orderPrice', 'orderQuantity', 'bankName'

    def __init__(self):
        super(AccountBuyAbleReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.bankCode: str = None
        self.stockCode: str = None
        self.securitiesType: str = None
        self.marketType: str = None
        self.orderPrice: int = None
        self.orderQuantity: int = None
        self.bankName: str = None


class AccountBuyAbleRes(Base):
    __slots__ = 'depositAmount', 'virtualDepositAmount', 'buyableQuantity', 'buyingPower', \
                'stockValuationAmount', 'assetValuationAmount', 'orderBlockAmount', \
                'totalBlockAmount', 'marginLimitation', 'lackAmount'

    def __init__(self):
        super(AccountBuyAbleRes, self).__init__()
        self.depositAmount: float = None
        self.virtualDepositAmount: float = None
        self.buyableQuantity: float = None
        self.buyingPower: float = None
        self.stockValuationAmount: float = None
        self.assetValuationAmount: float = None
        self.orderBlockAmount: float = None
        self.totalBlockAmount: float = None
        self.marginLimitation: float = None
        self.lackAmount: float = None
