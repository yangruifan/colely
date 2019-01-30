#!/usr/bin/env python
# encoding:utf-8
# @Time   : 2017/6/10
# @Author : 茶葫芦
# @Site   : 
# @File   : HiTime.py

import time, datetime as dt

"""
封装一套完整的python常用日期函数(独立模块,python 2.7及python 3.6环境下测试通过):
"""

class HiTime():
    @classmethod
    def struct(cls, dtstr):  # 返回结构化时间
        if len(dtstr) > 10:
                time_tuple = dt.datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")
        else:
                time_tuple = dt.datetime.strptime(dtstr, "%Y-%m-%d")
        return time_tuple

    @classmethod
    def Day(cls, dtstr):  # The day (an integer between 1 and 31)
        return cls.struct(dtstr).day

    @classmethod
    def DayName(cls, dtstr, langue='hans'):  # The name of the day of the week,default lan is chinese
        if langue == 'hans':
            days = dict(zip(['0', '1', '2', '3', '4', '5', '6'],
                            ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']))
        else:
            days = dict(zip(['0', '1', '2', '3', '4', '5', '6'],
                            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))

        return days.get(str(cls.DayNumber(dtstr)))

    @classmethod
    def DayNumber(cls,
                  dtstr):  # A number representing the day of the week (for example, Sunday is 6 and Wednesday is 2)
        return cls.struct(dtstr).weekday()

    @classmethod
    def DaysAfter(cls, dtstr1, dtstr2):  # The number of days one date occurs after another
        return cls.struct(dtstr2).toordinal() - cls.struct(dtstr1).toordinal()

    @classmethod
    def Hour(cls, dtstr):  # The time from which you want to obtain the hour
        return cls.struct(dtstr).hour

    @classmethod
    def Minute(cls, dtstr):  # The time from which you want to obtain the minutes
        return cls.struct(dtstr).minute

    @classmethod
    def Month(cls, dtstr):  # The month (an integer between 1 and 12)
        return cls.struct(dtstr).month

    @classmethod
    def Now(cls):  # Compare a time to the system time or display the system time on the screen
        return dt.datetime.now()

    @classmethod
    def RelativeDate(cls, dtstr, ndays):  # The date that occurs n days after a given date,return date ,not datetime
        return dt.datetime.fromordinal(cls.struct(dtstr).toordinal() + ndays)

    @classmethod
    def RelativeTime(cls, dtstr, nsecs):  # The time that occurs n seconds after a given time.
        return cls.struct(dtstr) + dt.timedelta(seconds=nsecs)

    @classmethod
    def Second(cls, dtstr):  # The number of seconds in the seconds portion of a given time.
        return cls.struct(dtstr).second

    @classmethod
    def SecondAfter(cls, dtstr1, dtstr2):  # The number of seconds one time occurs after another.
        return time.mktime(time.strptime(dtstr2, "%Y-%m-%d %H:%M:%S")) - time.mktime(
            time.strptime(dtstr1, "%Y-%m-%d %H:%M:%S"))

    @classmethod
    def Today(cls):  # The current system date
        return str(dt.datetime.today())[0:10]

    @classmethod
    def Year(cls, dtstr):  # The year (an integer between 1000 and 3000)
        return cls.struct(dtstr).year


if __name__ == '__main__':
    # print(HiTime.DaysAfter('2017-07-30 23:22:10', '2017-06-30 23:22:09'))

    print (HiTime.Day('2017-06-11 23:22:13'))

    # print(HiTime.())
