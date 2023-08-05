from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base


class HeaderRequest:
    __slots__ = 'userId', 'name', 'branchCode', 'deptNo1', 'deptNm1', 'deptNo2', 'deptNm2', \
                'trCode', 'ipAddress', 'lineCount', 'mdmType', 'dummy', 'secCode', 'lang', 'agencyCode'

    def __init__(self):
        self.userId: str = ""
        self.name: str = ""
        self.branchCode: str = ""
        self.deptNo1: str = ""
        self.deptNm1: str = ""
        self.deptNo2: str = ""
        self.deptNm2: str = ""
        self.trCode: str = ""
        self.ipAddress: str = ""
        self.lineCount: str = ""
        self.mdmType: str = ""
        self.dummy: str = ""
        self.secCode: str = ""
        self.lang: str = ""
        self.agencyCode: str = ""

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.userId: str = data[:15].decode().strip()
        instance.name: str = data[15:55].decode().strip()
        instance.branchCode: str = data[55:58].decode().strip()
        instance.deptNo1: str = data[58:61].decode().strip()
        instance.deptNm1: str = data[61:81].decode().strip()
        instance.deptNo2: str = data[81:86].decode().strip()
        instance.deptNm2: str = data[86:106].decode().strip()
        instance.trCode: str = data[106:111].decode().strip()
        instance.ipAddress: str = data[111:126].decode().strip()
        instance.lineCount: str = data[126:129].decode().strip()
        instance.mdmType: str = data[129:131].decode().strip()
        instance.dummy: str = data[131:161].decode().strip()
        instance.secCode: str = data[161:164].decode().strip()
        instance.lang: str = data[164:167].decode().strip()
        instance.agencyCode: str = data[167:168].decode().strip()
        return instance

    @classmethod
    def from_request(cls, request: Request):
        instance = cls()
        instance.userId: str = request.headers.token.userData.username.lower()
        instance.name: str = request.headers.token.userData.username
        instance.branchCode: str = request.headers.token.userData.mngDeptCode
        instance.deptNo1: str = request.headers.token.userData.deptCode
        instance.deptNm1: str = ""
        instance.deptNo2: str = request.headers.token.userData.branchCode
        instance.deptNm2: str = ""
        instance.trCode: str = ""
        instance.ipAddress: str = ""
        instance.lineCount: str = ""
        instance.mdmType: str = ""
        instance.dummy: str = ""
        instance.secCode: str = ""
        instance.lang: str = ""
        instance.agencyCode: str = request.headers.token.userData.agencyNumber
        return instance

    @classmethod
    def from_request_and_config(cls, request: Request, tr_code: str = "", ip_address: str = "", line_count: str = "20",
                                mdm_type: str = "", sec_code: str = "", lang: str = "E"):
        instance = cls()
        instance.userId: str = request.headers.token.userData.username.lower()
        instance.name: str = request.headers.token.userData.username
        instance.branchCode: str = request.headers.token.userData.mngDeptCode
        instance.deptNo1: str = request.headers.token.userData.deptCode
        instance.deptNm1: str = ""
        instance.deptNo2: str = request.headers.token.userData.branchCode
        instance.deptNm2: str = ""
        instance.trCode: str = tr_code
        instance.ipAddress: str = ip_address
        instance.lineCount: str = line_count
        instance.mdmType: str = mdm_type
        instance.dummy: str = ip_address.ljust(15, " ") + instance.name.ljust(15, " ")
        instance.secCode: str = sec_code
        instance.lang: str = lang
        instance.agencyCode: str = request.headers.token.userData.agencyNumber
        return instance

    def to_string(self) -> str:
        data = self.userId[:15].ljust(15, " ")
        data += self.name[:40].ljust(40, " ")
        data += self.branchCode[:3].ljust(3, " ")
        data += self.deptNo1[:5].ljust(5, " ")
        data += self.deptNm1[:20].ljust(20, " ")
        data += self.deptNo2[:3].ljust(3, " ")
        data += self.deptNm2[:20].ljust(20, " ")
        data += self.trCode[:5].ljust(5, " ")
        data += self.ipAddress[:15].ljust(15, " ")
        data += self.lineCount[:3].rjust(3, "0")
        data += self.mdmType[:2].ljust(2, " ")
        data += self.dummy[:30].ljust(30, " ")
        data += self.secCode[:3].ljust(3, " ")
        data += self.lang[:1].ljust(1, " ")
        data += self.agencyCode[:3].ljust(3, " ")
        return data

