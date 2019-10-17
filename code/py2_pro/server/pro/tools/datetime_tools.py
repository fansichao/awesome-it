# -*- coding=utf-8- -*-
u'''通用日期操作
    
    - str2date: 字符转换为日期格式
    - date2str: 日期格式换为字符转
    - str2datetime: 字符转换为日期时间格式
    - datetime2str: 日期格式转为字符串
    - str2timestamp: 字符转换为时间戳格式
    - get_first_date_of_month: 获取指定月份第一日
    - get_last_date_of_month: 获取指定月份最后一日
    - calc_date: 根据差值计算日期
    - cmp_date: 计算字符日期格式差距

    - date_dim_handler: 日期维度表处理
    - time_dim_handler: 时间维度表处理

'''
import time
import datetime
import logging


__author__ = "MQZhang"
__maintainer__ = "MQZhang"
__version__ = '0.1'
__all__ = ['str2date', 'date2str', 'str2datetime', 'get_first_date_of_month',
           'str2timestamp', 'timestamp2str', 'get_last_date_of_month', 'calc_date',
           'cmp_date', 'date_dim_handler', 'time_dim_handler']


def is_valid_date(strdt, strformat="%Y-%m-%d"):
    try:
        rv = datetime.datetime.strptime(strdt, strformat)
        return True
    except:
        return False


def str2date(dt, strformat="%Y-%m-%d"):
    rv = None
    if not bool(dt):
        return None

    dt = str(dt)
    if dt in ('00000000', '000000000.00'):
        rv = datetime.datetime(1900, 01, 01).date()
    else:
        if "-" in dt and ":" not in dt:
            strformat = "%Y-%m-%d"
        elif "/" in dt:
            strformat = "%Y/%m/%d"
        elif len(dt) == 8:
            strformat = "%Y%m%d"
        rv = datetime.datetime.strptime(dt, strformat).date()
    return rv


def date2str(dt, strformat="%Y-%m-%d"):
    return dt.strftime(strformat)


def str2int(dt_str):
    u"""将日期转换为整形"""
    return int(date2str(str2date(dt_str), "%Y%m%d"))


def str2datetime(dt, strformat="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(dt, strformat)


def datetime2str(dt):
    return str(dt)[0:19]
    # return str(datetime.datetime.strptime(dt, strformat))


def str2timestamp(dt, strformat="%Y-%m-%d %H:%M:%S"):
    u"""del文件中 描述为timestamp的源数据为8位数字 073000代表07:30:00 """
    # return datetime.datetime.strptime(dt, strformat).time()
    try:
        t = None
        if bool(dt.strip()):
            t = datetime.datetime.strptime(dt, strformat).time()
    except ValueError, e:
        logging.error(e)
        t = None
    return t


def timestamp2str(dt, strformat='%Y-%m-%d %H:%M:%S'):
    timeArray = time.localtime(dt)
    t = time.strftime(strformat, timeArray)
    return t


def get_first_date_of_month(year, month, strformat='%Y-%m-%d', str_flag=True):
    dt = datetime.date(int(year), int(month), 1)
    return dt.strftime(strformat) if str_flag else dt


def get_last_date_of_month(year, month, strformat='%Y-%m-%d', str_flag=True):
    month_end_dt = datetime.date(1900, 01, 01)
    if int(month) == 12:
        month_end_dt = datetime.date(
            int(year) + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        month_end_dt = datetime.date(int(year), int(
            month) + 1, 1) - datetime.timedelta(days=1)

    return month_end_dt.strftime(strformat) if str_flag else month_end_dt


def next_month(dt, strformat='%Y%m', to_strformat='%Y%m'):
    dt = str2date(str(dt), strformat)
    dt = calc_date(get_last_date_of_month(
        dt.year, dt.month, str_flag=False), 1)
    return date2str(dt, to_strformat)


def calc_date(date, delta=1, strformat=None):
    u'''计算新日期值 
        Arguments:
        - date: 基础日期，可为字符串日期格式，需指定strformat
        - delta: 与基础日期差值天数
        - strformat: 字符串日期格式
    '''
    if strformat:
        date = str2date(date, strformat)
    return date + datetime.timedelta(days=delta)


def cmp_date(dt1, dt2, dt1_strformat=None, dt2_strformat=None):
    u''' 计算日期差值 '''
    if dt1_strformat:
        dt1 = str2date(dt1, dt1_strformat)
    if dt2_strformat:
        dt2 = str2date(dt2, dt2_strformat)
    t_delta = dt1 - dt2
    return t_delta.days

# def get_deadline(run_date):
#    u''' 获取统计截止日期 '''
#    deadline = ''
#    if int(run_date[5:7]) + 1 >12:
#        deadline = str(int(run_date[:4])+1) +'-01-01'
#    else:
#        deadline = run_date[:4] + '-' + str(int(run_date[5:7])+1).zfill(2) +'-01'
#    return deadline


def date_dim_handler(date, date_col=None, strformat='%Y-%m-%d'):
    ''' For D_S_Date Dim, 将日期拆分为年、月、日、ISO周数、ISO星期数'''

    if date_col is None:
        date_col = ["date", "year", "month", "day", "week", "weekday", "monthendday",
                    "ispersonholiday", "isorgholiday", "yearday", "monthday", "source_table", "source_date"]

    if not bool(date):
        return dict(list(zip(date_col, [None] * len(date_col))))

    year = month = day = hour = minute = second = weekday = dayinyear = dst = yearday = monthday = ispersonholiday = isorgholiday = None
    isoyear = isoweek = isoweekday = None
    date_value = None
    row = {}
    if isinstance(date, datetime.datetime):
        (year, month, day, hour, minute, second,
         weekday, dayinyear, dst) = date.timetuple()
        (isoyear, isoweek, isoweekday) = date.isocalendar()
        date_value = date.strftime('%Y%m%d')

    if isinstance(date, basestring) and strformat:
        date_strformat = {8: "%Y%m%d",
                          10: "%Y-%m-%d",
                          14: "%Y%m%d%H%M%S",
                          25: {":": "%Y-%m-%d %H:%M:%S.%f", ".": "%Y-%m-%d %H.%M.%S.%f"},
                          26: "%Y-%m-%d-%H.%M.%S.%f"}
        try:
            if date == '00000000':
                date = date2str(datetime.datetime(
                    1900, 01, 01).date(), "%Y%m%d")

            strformat = date_strformat.get(len(date))
            without_blank_date = date.replace(' ', '')
            if len(without_blank_date) < len(date):
                strformat = date_strformat.get(len(without_blank_date))
                if len(without_blank_date) == 25:
                    strformat = strformat.get(
                        ":") if ":" in date else strformat.get(".")

            (year, month, day, hour, minute, second, weekday,
             dayinyear, dst) = time.strptime(str(date), strformat)
            (isoyear, isoweek, isoweekday) = datetime.date(
                year, month, day).isocalendar()
            date_value = str(date)
        except Exception, e:
            logging.debug(e)
            logging.info('日期格式错误:%s' % date)

    row['date'] = str2date(date_value, strformat)
    row['day'] = day
    row['month'] = month
    row['year'] = year
    row['week'] = isoweek
    row['weekday'] = isoweekday
    if month:
        if int(month) == 12:
            month_end_dt = datetime.date(
                int(year) + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            month_end_dt = datetime.date(int(year), int(
                month) + 1, 1) - datetime.timedelta(days=1)
        row['monthendday'] = datetime.date(
            int(year), int(month), month_end_dt.day)
        row['dateid'] = dayinyear + 366 * (year - 1990)
        row['yearday'] = (datetime.date(year=year, month=month, day=day) -
                          datetime.date(year=year, month=1, day=1)).days + 1
        row['monthday'] = day
        row['ispersonholiday'] = None
        row['isorgholiday'] = None

    for key in date_col:
        if key not in row.keys():
            row.update({key: None})

    return row


def time_dim_handler(time_str, time_col=None, strformat="%Y-%m-%d-%H.%M.%S.%f"):
    ''' For D_S_Time Dim, 将日期拆分为时，分，秒，上午，下午，中午，午夜'''
    # TODO 上午，下午，中午，午夜 分别代表什么意思? 怎么存

    if time_col is None:
        time_col = ["timestr", "hour", "minute",
                    "range", "source_table", "source_date"]

    if not bool(time_str):
        return dict(list(zip(time_col, [None] * len(time_col))))

    hour = minute = second = afternoon = night = midnight = morning = None
    row = {}

    # TODO
    if isinstance(time_str, datetime.time):
        pass

    if isinstance(time_str, basestring) and strformat:
        try:
            time_strformat = {6: "%H%M%S",
                              8: {":": "%H:%M:%S", "": "%H%M%S%f", '.': '%H.%M.%S'},
                              18: {"": "%Y-%m-%d %H:%M:%S"},
                              25: {":": "%Y-%m-%d %H:%M:%S.%f", ".": "%Y-%m-%d %H.%M.%S.%f"},
                              26: {"": "%Y-%m-%d %H.%M.%S.%f", '.': "%Y-%m-%d-%H.%M.%S.%f"}}
            strformat = time_strformat.get(len(time_str))
            without_blank_time = time_str.replace(' ', '')
            if len(without_blank_time) < len(time_str):
                strformat = time_strformat.get(len(without_blank_time))
                if len(without_blank_time) == 25:
                    strformat = strformat.get(
                        ":") if ":" in time_str else strformat.get(".")
                elif len(without_blank_time) == 18:
                    strformat = strformat.get("")
            if len(without_blank_time) == 6:
                strformat = strformat

            if len(without_blank_time) == 8:
                if ":" in time_str:
                    strformat = strformat.get(":")
                elif '.' in time_str:
                    strformat = strformat.get(".")
                else:
                    strformat = strformat.get("")

            if len(without_blank_time) == 26:
                strformat = strformat.get(
                    "") if " " in time_str else strformat.get(".")

            (year, month, day, hour, minute, second, weekday,
             dayinyear, dst) = time.strptime(str(time_str), strformat)

            row["timestr"] = str2timestamp(time_str, strformat)
            row['hour'] = hour
            row['minute'] = minute
            row['second'] = second
            row['range'] = None
        except Exception, e:
            logging.debug(e)
            logging.info('时间格式错误:%s' % time_str)

    for key in time_col:
        if key not in row.keys():
            row.update({key: None})

    return row


def get_now_datetime():
    u""" 获取当前时间 
    """
    now_time = datetime.datetime.now()
    return now_time


def time_show():
    u"""
    时间格式常用字符串
    #datetime、date、time都提供了strftime()方法，该方法接收一个格式字符串，输出日期时间的字符串表示
    strftime(...)
    strftime(format[, tuple]) -> string
    将指定的struct_time(默认为当前时间)，根据指定的格式化字符串输出
    python中时间日期格式化符号：
    %y 两位数的年份表示（00-99）
    %Y 四位数的年份表示（000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %I 12小时制小时数（01-12）
    %M 分钟数（00=59）
    %S 秒（00-59）
    %a 本地简化星期名称
    %A 本地完整星期名称
    %b 本地简化的月份名称
    %B 本地完整的月份名称
    %c 本地相应的日期表示和时间表示
    %j 年内的一天（001-366）
    %p 本地A.M.或P.M.的等价符
    %U 一年中的星期数（00-53）星期天为星期的开始
    %w 星期（0-6），星期天为星期的开始
    %W 一年中的星期数（00-53）星期一为星期的开始
    %x 本地相应的日期表示
    %X 本地相应的时间表示
    %Z 当前时区的名称
    %% %号本身
    """

    # 得到 时间戳timestamp
    print time() 
    # 由时间戳 得到 时间字符串
    print ctime() 
    # 由 struct_time 得到 时间戳timearray
    print mktime() 
    # 由 时间戳 得到 struct_time
    print localtime() 
    # 由struct_time 得到标准化时间格式
    print strftime() 
    # 由标准化时间格式得到数组
    print strptime() 


import dateutil
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule
# 周一到周日
from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU
# 年月周日时分秒
from dateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY


def last_day_of_next_month(ddate):
    u""" 
    relativedelta 适合指定时间
    relativedelta 单数为指定日期 复数为加减日期
    """
    return now_time + relativedelta(months=2, day=1, days=-1)


def date_some(st, ed, freq, select):
    u""" 获取时间范围的特定时间
    rrule 适合处理指定范围特定时间
    """
    st = datetime.date(2010, 01, 1)
    ed = datetime.date(2010, 02, 01)
    rule_obj = rrule(WEEKLY, byhour=(1, 2), dtstart=st, until=ed)
    # 0 周一 6周日
    rule_obj = rrule(DAILY, byweekday=(0, 6), dtstart=st, until=ed)
    rule_obj = rrule(DAILY, byweekday=(MO, WE), dtstart=st, until=ed)
    return [i for i in rule_obj]
