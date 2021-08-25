import os
from dateutil import tz
from datetime import datetime


class InvalidTimezone(Exception):
    pass


def get_current_datetime(timezone):
    tzinfo = tz.gettz(timezone)
    d = datetime.now(tz=tzinfo)
    return d.isoformat()


def check_timezone(timezone):
    tzinfo = tz.gettz(timezone)
    if tzinfo is None:
        raise InvalidTimezone(f"Wrong timezone value: {timezone}")
