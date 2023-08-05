from ..errors.GeneralError import GeneralError
from .Base import Base
from typing import Dict, List, Optional


class UserData(Base):
    __slots__ = 'username', 'identifierNumber', 'branchCode', 'mngDeptCode', 'deptCode', \
                'agencyNumber', 'userType', 'caThumbprint', 'accountNumbers', 'userLevel'

    def __init__(self, username: Optional[str] = None, identifier_number: Optional[str] = None,
                 branch_code: str = None, mng_dept_code: str = None,
                 dept_code: str = None, agency_number: str = None, user_type: str = None, ca_thumbprint: str = None,
                 user_level: str = None):
        self.username: str = username
        self.identifierNumber: str = identifier_number
        self.branchCode: str = branch_code
        self.mngDeptCode: str = mng_dept_code
        self.deptCode: str = dept_code
        self.agencyNumber: str = agency_number
        self.userType: str = user_type
        self.caThumbprint: str = ca_thumbprint
        self.userLevel: str = user_level
        self.accountNumbers: List[str] = []


class Token(Base):
    __slots__ = 'userId', 'serviceCode', 'connectionId', 'serviceId', 'serviceName', 'clientId', 'serviceUserId', \
                'loginMethod', 'refreshTokenId', 'scopeGroupIds', 'serviceUsername', 'userData', 'platform', \
                'appVersion', 'osVersion'

    def __init__(self):
        super(Token, self).__init__()
        self.userId: int = None
        self.serviceCode: str = None
        self.connectionId: str = None
        self.serviceId: int = None
        self.serviceName: str = None
        self.clientId: str = None
        self.serviceUserId: int = None
        self.loginMethod: int = None
        self.refreshTokenId: int = None
        self.scopeGroupIds: List[int] = None
        self.serviceUsername: str = None
        self.userData: UserData = UserData()
        self.platform: str = None
        self.appVersion: str = None
        self.osVersion: str = None


class Header(Base):
    __slots__ = 'token', 'accept_language'

    def __init__(self):
        super(Header, self).__init__()
        self.token: Token = None
        self.accept_language: str = None

    def key_mapping(self) -> Dict[str, str]:
        return {
            'accept_language': 'accept-language'
        }

    def get_from_dict_mapping(self):
        return {
            'token': lambda item, dic, this: parse_token(item)
        }


class Request(Base):
    __slots__ = 'headers', 'sourceIp', 'deviceType'

    def __init__(self):
        super(Request, self).__init__()
        self.headers: Header = None
        self.sourceIp: str = None
        self.deviceType: str = None

    def get_from_dict_mapping(self):
        return {
            'headers': lambda item, dic, this: parse_headers(item)
        }

    def validate_account_number(self, account_number):
        if account_number not in self.headers.token.userData.accountNumbers:
            raise GeneralError('INVALID_ACCOUNT_NUMBER')

    def get_ip(self):
        ip = self.sourceIp
        if self.sourceIp is not None:
            extend = "XU"  # undefined
            if self.headers.token.platform is None:
                extend = "XU"  # undefined
            elif self.headers.token.platform.lower() == 'android':
                extend = "XA"
            elif self.headers.token.platform.lower() == 'ios':
                extend = "XI"
            elif self.headers.token.platform.lower() == 'web':
                extend = "XW"

            if len(self.sourceIp) <= 13:
                ip = self.sourceIp + extend
            else:
                ip = self.sourceIp.replace('.', '', (len(self.sourceIp) - 13)) + extend
        return ip


def parse_headers(header_dict):
    return Header().from_dict(header_dict)


def parse_token(token_dict):
    return Token().from_dict(token_dict)
