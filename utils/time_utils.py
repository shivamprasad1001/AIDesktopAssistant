# utils/time_utils.py

from dateparser import parse

def normalize_date(raw_date):
    dt = parse(raw_date)
    return dt.strftime("%Y-%m-%d") if dt else None

def normalize_time(raw_time):
    dt = parse(raw_time)
    return dt.strftime("%H:%M") if dt else None
