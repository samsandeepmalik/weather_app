import calendar
import datetime
from datetime import date,timedelta


def convert_to_unix_time(datetime):
    return calendar.timegm(datetime.utctimetuple())


def get_past_datetime(days_to_minus):
    curr_dt = datetime.datetime.now()
    curr_date = datetime.date(curr_dt.year,curr_dt.month,curr_dt.day)
    old_date = (curr_date - timedelta(days_to_minus))
    old_dt = datetime.datetime(old_date.year,old_date.month,old_date.day)
    return old_dt


def convert_to_human_readable_format(unix_time):
    return datetime.datetime.utcfromtimestamp(unix_time)


def convert_date_format(timestamp, format='%Y-%m-%d'):
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return dt.strftime(format)


def format_datetime(date, dt_format: str = '%Y-%m-%d'):
    return date.strftime(dt_format)


# days=10
# print(get_past_datetime(days))
# past_dt = get_past_datetime(days)
#
# print("Unix Time : ", convert_to_unix_time(past_dt))
#
# print("Human Readable format : ", convert_to_human_readable_format(convert_to_unix_time(past_dt)))