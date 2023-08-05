from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountInfoReq(Request):
    __slots__ = 'accountNumber', 'subNumber'

    def __init__(self):
        super(AccountInfoReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None


class AccountInfoRes(Base):
    __slots__ = 'customerName', 'identifierNumber', 'identifierIssueDate', 'identifierIssuePlace', 'agencyCode', \
                'email', 'address', 'phoneNumber', 'dateOfBirth', 'accountType', 'agencyName', 'groupType', \
                'agencyBranch', 'representativeIdentifierNumber', 'representativeName', 'representativePhoneNumber', \
                'representativeEmail', 'countryCode', 'openBranchCode', 'openBranchName'

    def __init__(self):
        super(AccountInfoRes, self).__init__()
        self.customerName: str = None
        self.identifierNumber: str = None
        self.identifierIssueDate: str = None
        self.identifierIssuePlace: str = None
        self.agencyCode: str = None
        self.email: str = None
        self.address: str = None
        self.phoneNumber: str = None
        self.dateOfBirth: str = None
        self.accountType: str = None
        self.agencyName: str = None
        self.groupType: str = None
        self.agencyBranch: str = None
        self.representativeIdentifierNumber: str = None
        self.representativeName: str = None
        self.representativePhoneNumber: str = None
        self.representativeEmail: str = None
        self.countryCode: str = None
        self.openBranchCode: str = None
        self.openBranchName: str = None
