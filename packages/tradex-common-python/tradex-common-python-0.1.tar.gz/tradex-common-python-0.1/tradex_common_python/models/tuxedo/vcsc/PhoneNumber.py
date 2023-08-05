from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class PhoneNumberReq(Request):
    __slots__ = 'accountNumber'

    def __init__(self):
        super(PhoneNumberReq, self).__init__()
        self.accountNumber: str = None


class PhoneNumberRes(Base):
    __slots__ = 'phoneNumber'

    def __init__(self):
        super(PhoneNumberRes, self).__init__()
        self.phoneNumber: str = None
