import time
import datetime
from typing import Optional

DEFAULT_DATETIME_FORMAT: str = '%Y%m%d%H%M%S'
DEFAULT_DATE_FORMAT: str = '%Y%m%d'
DEFAULT_TIME_FORMAT: str = '%H%M%S'


def get_current_time_in_ms():
    return int(round(time.time() * 1000))


def convert_str_to_datetime(date_time_str: str, format_datetime: Optional[str] = DEFAULT_DATETIME_FORMAT) -> datetime:
    date_time_obj = datetime.datetime.strptime(date_time_str, format_datetime)
    return date_time_obj
