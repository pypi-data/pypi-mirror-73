import math
from datetime import datetime


def not_null_or_empty(s: str):
    return False if (s is None or s == '') else True


def obrigatory_text(s: str, min_len :int=5):
    return True if (not_null_or_empty(s) and len(s) >= min_len) else False


def obrigatory_number(n):
    return False if (n is None or math.isnan(n)) else True


def is_date_valid(d):
    try:
        datetime.strptime(d, '%d/%m/%Y')
        return True
    except Exception:
        return False


def is_time_valid(t):
    try:
        datetime.strptime(t, '%H/%M/%S')
        return True
    except Exception:
        return False


def is_datetime_valid(dt):
    try:
        datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
        return True
    except Exception:
        return False
