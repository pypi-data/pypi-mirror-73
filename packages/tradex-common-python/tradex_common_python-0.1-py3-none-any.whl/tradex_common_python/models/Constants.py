import enum

MARKET_TIME_ZONE_INT = 7


class AccountSubTypeEnum(enum.Enum):
    DERIVATIVES: str = "DERIVATIVES"
    EQUITY: str = "EQUITY"


class SecuritiesTypeEnum(enum.Enum):
    STOCK = '01'
    BOND = '02'
    FUND = '03'
    ETF = '03'
    CW = '07'
    ALL = '%'


class SellBuyTypeEnum(enum.Enum):
    BUY = '2'
    SELL = '1'
    ALL = '%'


class DrSellBuyTypeEnum(enum.Enum):
    BUY = '1'
    SELL = '2'


class DrOrderTypeEnum(enum.Enum):
    MP = '1'
    LO = '2'
    ATO = '3'
    MAK = '4'
    MOK = '5'
    ATC = '6'
    MTL = 'K'


class ValidityEnum(enum.Enum):  # Matched condition
    DAY = '0'
    GTC = '1'
    GTD = '6'


class DrValidityTypeEnum(enum.Enum):
    DAY = 'O'
    ATO = '2'
    IOC = '3'
    FOK = '4'
    ATC = '7'


class DrTransferImFeeTypeEnum(enum.Enum):
    INCLUSIVE = 'I'
    EXCLUSIVE = 'E'


class DrAdvOrderMarketSessionEnum(enum.Enum):
    ATO = '1'
    MORNING = '2'
    AFTERNOON = '3'
    ATC = '4'


class DrAdvOrderTypeEnum(enum.Enum):
    AO = '1'
    CAO = '2'


class MatchTypeEnum(enum.Enum):
    MATCHED = '1'
    UNMATCHED = '2'
    ALL = '%'


class OddlotMatchTypeEnum(enum.Enum):
    MATCHED = '2'
    UNMATCHED = '1'
    ALL = '0'


class OrderTypeEnum(enum.Enum):
    LO = '01'
    MP = '02'
    ATO = '03'
    ATC = '04'
    AON = '05'
    BIG_LOT = '06'
    MOK = '07'
    MAK = '08'
    MTL = '09'
    IO = '10'
    SO_GREATER = '11'
    SO_LESS = '12'
    SBO = '13'
    OBO = '14'
    PLO = '15'
    ALL = '%'


class MarketTypeEnum(enum.Enum):
    HOSE = 1
    HNX = 2
    UPCOM = 4
    ALL = '%'


class SortTypeEnum(enum.Enum):
    DESC = 'D'
    ASC = 'A'


class OrderStatusEnum(enum.Enum):
    RECEIPT = '0'
    SEND = '1'
    ORDER_CONFIRM = '2'
    RECEIPT_CONFIRM = '3'
    FULL_FILLED = '4'
    PARTIAL_FILLED = '5'
    REJECT = 'X'


class OrderModifyCancelTypeEnum(enum.Enum):
    SELL = '1'
    BUY = '2'
    MODIFY_OF_SELL = '3'
    MODIFY_OF_BUY = '4'
    CANCEL_OF_SELL = '5'
    CANCEL_OF_BUY = '6'


class RightTypeEnum(enum.Enum):
    ADDITIONAL_STOCK: str = 'ADDITIONAL_STOCK'
    BOND: str = 'BOND'
    ALL: str = ''


class WithdrawStatusEnum(enum.Enum):
    PENDING: str = 'c'
    CANCELLED: str = 'd'
    APPROVED: str = 'e'


class TransferCashStatusEnum(enum.Enum):
    PENDING: str = 'c'
    CANCELLED: str = 'd'
    APPROVED: str = 'e'
    APPROVED_INTERNAL: str = 'f'


class InternalExternalEnum(enum.Enum):
    INTERNAL: str = 'INTERNAL'
    EXTERNAL: str = 'EXTERNAL'


class DrImBankQueryTypeEnum(enum.Enum):
    DEPOSIT_FROM = 'A'
    DEPOSIT_TO = 'B'
    WITHDRAW_FROM = 'C'
    WITHDRAW_TO = 'D'


class DrImFeeQueryTypeEnum(enum.Enum):
    DEPOSIT = 'C05'
    WITHDRAW = 'C10'


class DrImHistoryQueryTypeEnum(enum.Enum):
    DEPOSIT = 'C05'
    WITHDRAW = 'C10'


class UserDataEnum(enum.Enum):
    ORDER_PASS: str = 'ORDER_PASS'
    IDENTIFIER_NUMBER: str = 'IDENTIFIER_NUMBER'
    BRANCH_CODE: str = 'BRANCH_CODE'
    MNG_DEPT_CODE: str = 'MNG_DEPT_CODE'
    DEPT_CODE: str = 'DEPT_CODE'
    AGENCY_NUMBER: str = 'AGENCY_NUMBER'
    USER_TYPE: str = 'USER_TYPE'


class MarginLevelEnum(enum.Enum):
    NORMAL: str = '0'
    WARNING_LEVEL_1: str = '1'
    WARNING_LEVEL_2: str = '2'
    WARNING_LEVEL_3: str = '3'
