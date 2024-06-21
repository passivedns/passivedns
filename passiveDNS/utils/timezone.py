from dateutil import tz
from datetime import datetime, date, timezone
import logging


class InvalidTimezone(Exception):
    pass


def get_current_datetime(timezone):
    tzinfo = tz.gettz(timezone)
    d = datetime.now(tz=tzinfo)
    return d.isoformat()


def to_current_timezone(timez: str, date: date):
    out = date.replace(tzinfo=timezone.utc)
    tzinfo = tz.gettz(timez)
    out = out.astimezone(tzinfo)
    return out.isoformat()


def check_timezone(timezone):
    tzinfo = tz.gettz(timezone)
    if tzinfo is None:
        logging.error("Invalid timezone: {}".format(timezone))
        tzinfo = tz.gettz("UTC")
