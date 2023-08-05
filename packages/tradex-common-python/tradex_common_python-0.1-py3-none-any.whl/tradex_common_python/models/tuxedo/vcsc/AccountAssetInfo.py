from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountAssetInfoReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'bankCode', 'bankAccount'

    def __init__(self):
        super(AccountAssetInfoReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.bankCode: str = None
        self.bankAccount: str = None


class AccountAssetInfoRes(Base):
    __slots__ = 'netAsset', 'totalAsset', 'totalCash', 'availableCash', 'unavailableCash', \
                'reuseAmount', 'dividend', 'stockEvaluationAmount', 'availableStockAmount', \
                'unavailableStockAmount', 'buyingStockWaitingAmount', 'rights', 'pendingStockAmount', \
                'totalLoanAmount', 'marginLoan', 'nonSettledBuyingAmount', 'unmatchBuyingAmount', 'interest', \
                'depositoryFee', 'minBuyingPower', 'withdrawableAmount', 'cmr', 'cashAmountForMMR', \
                'stockAmountForMMR', 'virtualDeposit', 'usedVirtualDeposit', 'totalLackingSettledAmount', \
                'lackingMarginAmount', 'lackingVirtualDepositAmount', 'lackingLoanAmountForT1', \
                'marginAvailableStockAmount', 'marginUnavailableStockAmount', 'marginRights', \
                'marginPendingStockAmount', 'evaluationAvailableStockAmount', 'evaluationUnavailableStockAmount', \
                'evaluationRights', 'evaluationPendingStockAmount', 'totalLoanMortgage', 'totalLoanBuying', \
                'totalLoanExpectedAmount', 'stockAmountCanUseMargin', 'evaluationAmount', 'tlTaOfTotalAccount', \
                'tlTaOfMarginList'

    def __init__(self):
        super(AccountAssetInfoRes, self).__init__()
        self.netAsset: float = None
        self.totalAsset: float = None
        self.netAsset: float = None
        self.totalAsset: float = None
        self.totalCash: float = None
        self.availableCash: float = None
        self.unavailableCash: float = None
        self.reuseAmount: float = None
        self.dividend: float = None
        self.stockEvaluationAmount: float = None
        self.availableStockAmount: float = None
        self.unavailableStockAmount: float = None
        self.buyingStockWaitingAmount: float = None
        self.rights: float = None
        self.pendingStockAmount: float = None
        self.totalLoanAmount: float = None
        self.marginLoan: float = None
        self.nonSettledBuyingAmount: float = None
        self.unmatchBuyingAmount: float = None
        self.interest: float = None
        self.depositoryFee: float = None
        self.minBuyingPower: float = None
        self.withdrawableAmount: float = None
        self.cmr: float = None
        self.cashAmountForMMR: float = None
        self.stockAmountForMMR: float = None
        self.virtualDeposit: float = None
        self.usedVirtualDeposit: float = None
        self.totalLackingSettledAmount: float = None
        self.lackingMarginAmount: float = None
        self.lackingVirtualDepositAmount: float = None
        self.lackingLoanAmountForT1: float = None
        self.marginAvailableStockAmount: float = None
        self.marginUnavailableStockAmount: float = None
        self.marginRights: float = None
        self.marginPendingStockAmount: float = None
        self.evaluationAvailableStockAmount: float = None
        self.evaluationUnavailableStockAmount: float = None
        self.evaluationPendingStockAmount: float = None
        self.evaluationRights: float = None
        self.totalLoanMortgage: float = None
        self.totalLoanBuying: float = None
        self.totalLoanExpectedAmount: float = None
        self.stockAmountCanUseMargin: float = None
        self.evaluationAmount: float = None
        self.tlTaOfTotalAccount: float = None
        self.tlTaOfMarginList: float = None
