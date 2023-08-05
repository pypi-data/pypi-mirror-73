class GridHeader:
    __slots__ = 'inputKey', 'sortDirection', 'location', 'continueFlag', 'rows', 'nextKey'

    def __init__(self):
        super(GridHeader, self).__init__()
        self.inputKey: str = ""
        self.sortDirection: str = ""
        self.location: str = ""
        self.continueFlag: str = ""
        self.rows: str = ""
        self.nextKey: str = ""

    @classmethod
    def from_bytes(cls, data: bytes):
        instance = cls()
        instance.inputKey: str = ""
        instance.sortDirection: str = data[0:1].decode().strip()
        instance.location: str = data[1:2].decode().strip()
        instance.continueFlag: str = data[2:3].decode().strip()
        # ignore one special byte
        instance.rows: str = data[4:8].decode().strip()
        instance.nextKey: str = data[8:78].decode().strip()
        return instance
