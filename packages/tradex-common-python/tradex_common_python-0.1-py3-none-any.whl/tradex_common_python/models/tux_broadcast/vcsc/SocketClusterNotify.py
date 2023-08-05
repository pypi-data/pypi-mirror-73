from tradex_common_python.models.Base import Base
from typing import Dict


class SocketClusterNotify(Base):
    __slots__ = 'method', 'template', 'configuration'

    def __init__(self):
        super(SocketClusterNotify, self).__init__()
        self.method: str = None
        self.configuration: str = None
        self.template: Dict = None
