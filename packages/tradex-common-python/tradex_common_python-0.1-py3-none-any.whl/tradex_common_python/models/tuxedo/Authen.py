from ..Request import Request, UserData
from ..Base import Base
from typing import List


class AuthenReq(Request):
    __slots__ = 'username', 'password', 'systemName'

    def __init__(self):
        super(AuthenReq, self).__init__()
        self.username: str = None
        self.password: str = None
        self.systemName: str = None


class Bank(Base):
    __slots__ = 'bankCode', 'bankName'

    def __init__(self):
        super(Bank, self).__init__()
        self.bankCode: str = None
        self.bankName: str = None


class AccountSub(Base):
    __slots__ = 'subNumber', 'bankAccounts', 'type'

    def __init__(self):
        super(AccountSub, self).__init__()
        self.subNumber: str = None
        self.type: str = None
        self.bankAccounts: List[Bank] = None


class Account(Base):
    __slots__ = 'accountNumber', 'accountName', 'accountSubs'

    def __init__(self):
        super(Account, self).__init__()
        self.accountNumber: str = None
        self.accountName: str = None
        self.accountSubs: List[AccountSub] = None


class UserInfo(Base):
    __slots__ = 'username', 'identifierNumber', 'accounts', 'caThumbprint', 'userLevel'

    def __init__(self):
        super(UserInfo, self).__init__()
        self.username: str = None
        self.identifierNumber: str = None
        self.accounts: List[Account] = None
        self.caThumbprint: str = None
        self.userLevel: str = None


class AuthenRes(Base):
    __slots__ = 'conId', 'userInfo', 'otpIndex', 'otpValue', 'userData'

    def __init__(self):
        super(AuthenRes, self).__init__()
        self.conId: str = None
        self.userInfo: UserInfo = None
        self.otpIndex: str = None
        self.otpValue: str = None
        self.userData: UserData = UserData()


class AccountListReq(Request):
    __slots__ = 'lastAccountNumber', 'lastSubNumber', 'fetchCount'

    def __init__(self):
        super(AccountListReq, self).__init__()
        self.lastAccountNumber: str = None
        self.lastSubNumber: str = None
        self.fetchCount: int = None
