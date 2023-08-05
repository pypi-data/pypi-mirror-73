from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class DrAccountRiskRatioReq(Request):
    __slots__ = 'accountNumber'

    def __init__(self):
        super(DrAccountRiskRatioReq, self).__init__()
        self.accountNumber: str = None


class DrAccountRiskRatioRes(Base):
    __slots__ = 'acceptedCollateralValue', 'initialMargin', 'variationMargin', 'spreadMargin', \
                'initialMarginDelivery',  'marginRequirement', 'marginUtilization', 'position', 'marginLevel'

    def __init__(self):
        super(DrAccountRiskRatioRes, self).__init__()
        self.acceptedCollateralValue: float = None
        self.initialMargin: float = None
        self.variationMargin: float = None
        self.spreadMargin: float = None
        self.initialMarginDelivery: float = None
        self.marginRequirement: float = None
        self.marginUtilization: float = None
        self.position: int = None
        self.marginLevel: str = None

