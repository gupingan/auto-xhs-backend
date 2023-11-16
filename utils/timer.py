"""
@File: timer.py
@Author: 秦宇
@Created: 2023/11/5 14:44
@Description: Created in 咸鱼-自动化-AutoXhs.
"""
import time
from datetime import datetime, timedelta


def timeText(timestamp, template: str = "%Y-%m-%d %H:%M:%S"):
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_datetime = dt_object.strftime(template)
    return formatted_datetime


def current(type_: str = 'datetime', template: str = "%Y-%m-%d %H:%M:%S"):
    now = datetime.now()
    if type_ == 'str':
        return now.strftime(template)
    elif type_ == 'datetime':
        return now
    elif type_ == 'timestamp':
        return int(now.timestamp())
    return None


def after(minutes, type_: str = 'datetime', template: str = "%Y-%m-%d %H:%M:%S"):
    now = datetime.now()
    future_time = now + timedelta(minutes=minutes)
    if type_ == 'str':
        return future_time.strftime(template)
    elif type_ == 'datetime':
        return future_time
    return None


def ltOneMinute(timestamp):
    now = datetime.now()
    current_time = datetime.fromtimestamp(float(timestamp))
    time_difference = now - current_time
    return time_difference > timedelta(minutes=1)


def remainSeconds(future_time: datetime):
    return (future_time - datetime.now()).seconds


if __name__ == '__main__':
    t1 = after(5)
    print(remainSeconds(t1))
