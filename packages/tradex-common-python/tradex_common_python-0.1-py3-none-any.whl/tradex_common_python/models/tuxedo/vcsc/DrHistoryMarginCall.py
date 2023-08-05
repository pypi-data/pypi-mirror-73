from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrHistoryMarginCallReq(Request):
    __slots__ = 'accountNumber', 'fromDate', 'toDate', 'lastNextKey', 'fetchCount'

    def __init__(self):
        super(DrHistoryMarginCallReq, self).__init__()
        self.accountNumber: str = None
        self.fromDate: str = None
        self.toDate: str = None
        self.lastNextKey: str = None
        self.fetchCount: int = None


class DrHistoryMarginCallRes(Base):
    __slots__ = 'date', 'marginRequirement', 'previousDepositBalance', 'previousAssignedCAA', 'previousMarginDeficit', \
                'depositBalance', 'assignedCAA', 'marginAmount', 'netMarginCall', 'isResolved', 'nextKey'

    def __init__(self):
        super(DrHistoryMarginCallRes, self).__init__()
        self.date: str = None
        self.marginRequirement: float = None
        self.previousDepositBalance: float = None
        self.previousAssignedCAA: float = None
        self.previousMarginDeficit: float = None
        self.depositBalance: float = None
        self.assignedCAA: float = None
        self.marginAmount: float = None
        self.netMarginCall: float = None
        self.isResolved: bool = None
        self.nextKey: str = None
