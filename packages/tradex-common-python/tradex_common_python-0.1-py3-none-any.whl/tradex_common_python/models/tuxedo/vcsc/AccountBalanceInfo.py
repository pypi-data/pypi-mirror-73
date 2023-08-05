from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountBalanceInfoReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'bankCode', 'bankAccount'

    def __init__(self):
        super(AccountBalanceInfoReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.bankCode: str = None
        self.bankAccount: str = None


class AccountBalanceInfoRes(Base):
    __slots__ = 'netAssetValue', 'currentCash', 'blockedCash', 'unsettledCash', 'unpaidDividend', 'totalAsset', \
                'currentHoldingValue', 'valueOfUnpaidRights', 'investedCapital', 'unrealisedPL', \
                'unrealisedPLRate', 'depositoryFee', 'marginLoan', 'mortgagedLoan', 'loanInterest', \
                'unsettledBuyingAmount', 'totalDebt'

    def __init__(self):
        super(AccountBalanceInfoRes, self).__init__()
        self.netAssetValue: float = None
        self.currentCash: float = None
        self.blockedCash: float = None
        self.unsettledCash: float = None
        self.unpaidDividend: float = None
        self.totalAsset: float = None
        self.currentHoldingValue: float = None
        self.valueOfUnpaidRights: float = None
        self.investedCapital: float = None
        self.unrealisedPL: float = None
        self.unrealisedPLRate: float = None
        self.depositoryFee: float = None
        self.marginLoan: float = None
        self.mortgagedLoan: float = None
        self.loanInterest: float = None
        self.unsettledBuyingAmount: float = None
        self.totalDebt: float = None
