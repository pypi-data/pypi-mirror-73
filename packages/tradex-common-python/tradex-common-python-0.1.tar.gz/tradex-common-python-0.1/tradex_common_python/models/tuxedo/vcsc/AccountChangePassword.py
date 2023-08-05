from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountChangePasswordReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'oldPassword', 'newPassword'

    def __init__(self):
        super(AccountChangePasswordReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.oldPassword: str = None
        self.newPassword: str = None


class AccountChangePasswordRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(AccountChangePasswordRes, self).__init__()
        self.message: str = None
