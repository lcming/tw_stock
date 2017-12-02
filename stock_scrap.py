#!/usr/bin/python3
import datetime

class stock_scrap:
    stock_id = None
    url = None
    trace_len = None
    today = None
    request_dates = []
    record_dates = []
    data = {}

    def __init__(self, _stock_id, _trace_len, _url):
        self.today = datetime.date.today()
        self.stock_id = _stock_id
        self.trace_len = _trace_len
        self.url = _url
        self.record_dates.clear()
        self.request_dates.clear()
        self.data.clear()

    def get_date_string(self, d):
        y_str = d.year
        m_str = str(0) + str(d.month) if len(str(d.month)) == 1 else str(d.month)
        d_str = str(0) + str(d.day) if len(str(d.day)) == 1 else str(d.day)
        return "%s%s%s" % (y_str, m_str, d_str)

    def set_today(self, y, m, d):
        new_date = datetime.date(y, m, d)
        self.today = new_date

    def dbg(self):
        print("Stock: %s, url: %s" % (self.stock_id, self.url))
        print("Request dates include:"),
        for date in self.request_dates:
            print("%s" % date),
        print("")
        print("Record dates include:"),
        for date in self.record_dates:
            print("%s" % date),
        print("")
    def get_daily_info(self, date):
        assert(False)

    def format_url(self, date):
        assert(False)

    def get_pure_int(self, number):
        import re
        pat = re.compile('\..*')
        number = pat.sub("", number)
        pat = re.compile('\D')
        number = pat.sub("", number)
        return int(number)
    def get_pure_float(self, number):
        import re
        pat = re.compile('((?=[^\.])\D)')
        number = pat.sub("", number)
        return float(number)






