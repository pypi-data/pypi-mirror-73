from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AgencyInfoReq(Request):
    __slots__ = 'accountNumber'

    def __init__(self):
        super(AgencyInfoReq, self).__init__()
        self.accountNumber: str = None


class AgencyInfoRes(Base):
    __slots__ = 'agencyCode', 'agencyName', 'agencyBranch'

    def __init__(self):
        super(AgencyInfoRes, self).__init__()
        self.agencyCode: str = None
        self.agencyName: str = None
        self.agencyBranch: str = None
