#coding=utf-8
from datetime import *

class timeTool:
    def __init__(self, in_time=None):
        if in_time is None:
            self._time = datetime.now()
        else:
            self._time = in_time
        self.__weekdays = ["monday", "tuesday", \
                           "wednesday", "thursday", \
                           "friday", "saturday","sunday" ]
        self.__months = ["january","february",\
                         "march","april",\
                         "may","june",\
                         "july","august", \
                         "september","october",\
                         "november","december"]
        self.__months_abbr = ["jan","feb",\
                         "mar","apr",\
                         "may","jun",\
                         "jul","aug", \
                         "sep","oct",\
                         "nov","dec"]
        self.__pattern_width = {'a':3,'b':3,'c':17}
        self.__pattern_width_A = {}
        self.__pattern_width_B = {'jan':7,"feb":8,\
                         "mar":5,"apr":5,\
                         "may":3,"jun":4,\
                         "jul":4,"aug":6, \
                         "sep":9,"oct":7,\
                         "nov":8,"dec":8}          
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, value):
        self._time = value
    
    @property
    def weekday(self):
        return self.time.strftime('%A')
    
    @property
    def weekday_abbr(self):
        return self.time.strftime('%a')
    
    @property
    def month_name(self):
        return self.time.strftime('%B')
    
    @property
    def month_name_abbr(self):
        return self.time.strftime('%b')
    
    def month_name_to_int(self, month_name, abbr=False):
        if abbr:
            name_list = self.__months_abbr
        else:
            name_list = self.__months            
        return name_list.index(month_name.lower())+1
    
    #--------------------------------------------------
    # 格式化字符串的意义：
    # %a 星期的简写。如 星期三为Web
    # %A 星期的全写。如 星期三为Wednesday
    # %b 月份的简写。如4月份为Apr
    # %B月份的全写。如4月份为April
    # %c:  日期时间的字符串表示。（如： 04/07/10 10:43:39）
    # %d:  日在这个月中的天数（是这个月的第几天）
    # %f:  微秒（范围[0,999999]）
    # %H:  小时（24小时制，[0, 23]）
    # %I:  小时（12小时制，[0, 11]）
    # %j:  日在年中的天数 [001,366]（是当年的第几天）
    # %m:  月份（[01,12]）
    # %M:  分钟（[00,59]）
    # %p:  AM或者PM
    # %S:  秒（范围为[00,61]，为什么不是[00, 59]，参考python手册~_~）
    # %U:  周在当年的周数当年的第几周），星期天作为周的第一天
    # %w:  今天在这周的天数，范围为[0, 6]，6表示星期天
    # %W:  周在当年的周数（是当年的第几周），星期一作为周的第一天
    # %x:  日期字符串（如：04/07/10）
    # %X:  时间字符串（如：10:43:39）
    # %y:  2个数字表示的年份
    # %Y:  4个数字表示的年份
    # %z:  与utc时间的间隔 （如果是本地时间，返回空字符串）
    # %Z:  时区名称（如果是本地时间，返回空字符串）
    # %%:  %% => %
    # ————————————————
    def formatted_string(self,t_time = None,pattern='full_underline'):
        if t_time is None:
            t_time = self._time
        elif t_time == 'now':
            t_time = datetime.now()
        if pattern=='full_blank':
            t_str = t_time.strftime("%Y %m %d %h %M %s")
        elif pattern == 'full':
            t_str = t_time.strftime("%Y%m%d%H%M%S")
        elif pattern == 'full_bar_colon':
            t_str = t_time.strftime("%Y-%m-%d %H:%M:%S")
        elif pattern == 'full_underline':
            t_str = t_time.strftime("%Y_%m_%d_%H_%M_%S")
        elif pattern == 'full_bar_colon_weekday':
            t_str = t_time.strftime("%Y-%m-%d") + \
                    self.week_day(t_time) + \
                    t_time.strftime("%H:%M:%S")
        elif pattern == 'full_underline_weekday':
            t_str = t_time.strftime("%Y_%m_%d_") + \
                    self.week_day(t_time) + \
                    t_time.strftime("_%H_%M_%S")
        elif pattern == 'ymd':
            t_str = t_time.strftime("%Y%m%d")
        elif pattern == 'ymd_blank':
            t_str = t_time.strftime("%Y %m %d")
        elif pattern == 'ymd_bar':
            t_str = t_time.strftime("%Y-%m-%d")
        elif pattern == 'ymd_underline':
            t_str = t_time.strftime("%Y_%m_%d")
        elif pattern == 'hms':
            t_str = t_time.strftime("%H%M%S")
        elif pattern == 'hms_blank':
            t_str = t_time.strftime("%H %M %S")
        elif pattern == 'hms_bar':
            t_str = t_time.strftime("%H-%M-%S")
        elif pattern == 'ymd_underline':
            t_str = t_time.strftime("%H_%M_%S")
        elif pattern == 'full_date':
            t_str = self.month_name(t_time) + " " + self.date(t_time) + \
                t_time.strftime(", %Y")
        elif pattern == 'full_date_time':
            t_str = t_time.strftime("%H:%M:%S, ") + \
                    self.month_name(t_time) + " " + self.date(t_time) + \
                    t_time.strftime(", %Y %H:%M:%S")
        elif pattern == 'full_abbr_date':
            t_str = self.abbr_month_name(t_time) + " " + self.date(t_time)
        elif pattern == 'full_abbr_date_time':
            t_str = t_time.strftime("%H:%M:%S, ") + self.abbr_month_name(t_time) + " " + self.date(t_time) + \
                t_time.strftime(", %Y")
        else:
            t_str = t_time.strftime(pattern)
        return t_str  
    
    #
    def formatted_string_to_time(self,time_str, pattern, inplace=False):
        p_list = pattern.split('%')
        for str in p_list:
            tmpw = []
        return p_list
    
            
        

class timer:
    def __init__(self, start_time=None):
        if start_time is None:
            self._start_time = datetime.now()
        else:
            self._start_time = start_time

        self._timings = []
        self._last_timing = self.start_time
        self._timing = self.start_time

        self.__weekdays = ["Monday", "Tuesday", \
                           "Wednesday", "Thursday", \
                           "Friday", "Saturday","Sunday" ]

        self.__months = ["January","February",\
                         "march","April",\
                         "May","June",\
                         "July","August", \
                         "September","October",\
                         "November","December"]

        self.__months_abbr = ["Jan","Feb",\
                         "mar","Apr",\
                         "May","Jun",\
                         "Jul","Aug", \
                         "Sep","Oct",\
                         "Nov","Dec"]

    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    def clear(self):
        self._start_time = datetime.now()
        self._start_time = []

    def week_day(self,t_time):
        return self.__weekdays[t_time.weekday]

    def month_name(self,t_time):
        m = t_time.month - 1
        return self.__months[m]

    def abbr_month_name(self,t_time):
        m = t_time.month - 1
        return self.__months_abbr[m]

    def abbr_name_to_month(self,m_name):
        tmp_name = m_name.lower()
        for i in range(12):
            if tmp_name == self.__months_abbr[i].lower():
                return i + 1
        return 0

    def date(self,t_time):
        d = t_time.day
        if d == 1:
            return "1st"
        elif d == 2:
            return "2nd"
        elif d == 3:
            return "3rd"
        else:
            return str(d) + "th"

    def year_days_to_date(self,year,days):
        new_year = datetime(year,1,1)
        new_day = new_year + datetime.timedelta(days=days - 1)
        return new_day

    def year_days_to_month_day(self,year,days):
        new_day = self.year_days_to_date(year,days)
        y = year
        m = new_day.month
        d = new_day.day
        return [y,m,d]


    def timing(self,from_time='last', record=False):
        if from_time=='last':
            time_begin = self._last_timing
        elif from_time=='start':
            time_begin = self._start_time
        else:
            index = int(from_time)
            time_begin = self._timings[index]
        self._last_timing = self._timing
        self._timing = datetime.now()
        if record:
            self._timings.append(self._timing)
        interval = self._timing - time_begin
        h = interval.seconds // 3600
        m = (interval.seconds - h * 3600) // 60
        s = interval.seconds - h * 3600 - m * 60
        print(self.formated_time_string(self._last_timing,"From [%Y-%m-%d %H:%M:%S]") +\
              "total %d hours %d minutes %d seconds past " % (h, m, s))

    def new_day(self,year, month, day):
        return datetime(year,month,day)




