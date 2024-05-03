import os
from dateutil import tz
from datetime import datetime
import logging

class InvalidTimezone(Exception):
    pass


def get_current_datetime(timezone):
    tzinfo = tz.gettz(timezone)
    d = datetime.now(tz=tzinfo)
    return d.isoformat()


def check_timezone(timezone):
    tzinfo = tz.gettz(timezone)
    if tzinfo is None:
       logging.error("Invalid timezone: {}".format(timezone)) 
       tzinfo = tz.gettz('UTC')
