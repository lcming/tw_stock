#!/usr/bin/python3

from lxml import etree, html
import logging
import pprint
import re
import datetime
from stock_scrap import stock_scrap

class price_scrap(stock_scrap):

    def __init__(self, _stock_id, _trace_len):
        _url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG'
        super().__init__(_stock_id, _trace_len, _url)

    def get_last_day_of_prev_month(self, d):
        old_d = d
        while (d.month == old_d.month):
            d -= datetime.timedelta(1)
        return d

    def format_date(self, date):
        # from 106/11/11 to 20171111
        y, m, d = date.split('/')
        y = int(y) + 1911
        return str(y) + str(m) + str(d)

    def set_daily_info(self, date):
        raw_data = eval(self.get_html_str(self.format_url(date)))
        data_part = raw_data['data']
        for day_info in data_part:
            if(re.match('\d+/\d+/\d+', day_info[0])):
                formatted_date = self.format_date(day_info[0])
                price = self.get_pure_float(day_info[1])
                self.data[formatted_date] = price

    def format_url(self, date):
        _url = self.url + '?response=json&date=' + date + '&stockNo=' + str(self.stock_id)
        #http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303
        return _url

if __name__ == '__main__':
    ps = price_scrap("2303", 14)
    ps.set_data()

