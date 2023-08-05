from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class AccountChangeHTSPasswordReq(Request):
    __slots__ = 'username', 'newPassword', 'oldPassword'

    def __init__(self):
        super(AccountChangeHTSPasswordReq, self).__init__()
        self.username: str = None
        self.newPassword: str = None
        self.oldPassword: str = None


class AccountChangeHTSPasswordRes(Base):
    __slots__ = 'message'

    def __init__(self):
        super(AccountChangeHTSPasswordRes, self).__init__()
        self.message: str = None
