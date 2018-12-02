#!/usr/bin/python3

from lxml import etree, html
import logging
import pprint
import re
import datetime
from stock_scrap import stock_scrap

class index_scrap(stock_scrap):

    def __init__(self, _trace_len):
        _url = 'http://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json'
        super().__init__("_tw_index", _trace_len, _url)
        self.url2 = "http://www.twse.com.tw/exchangeReport/MI_5MINS?"

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
        url = self.format_url(date)
        raw_data = eval(self.get_html_str(url))
        try:
            data_part = raw_data['data']
        except KeyError:
            logging.error("No price info. on %s" % date)
            return
        for day_info in data_part:
            if(re.match('\d+/\d+/\d+', day_info[0])):
                formatted_date = self.format_date(day_info[0])
                if formatted_date == date:
                    self.data[formatted_date] = {}
                    # try to fill everyday available from URL
                    field = ['open', 'high', 'low', 'close']
                    offset = 1
                    for i in range(len(field)):
                        self.data[formatted_date][field[i]] = self.get_pure_float(day_info[i+offset])

        url = self.format_url2(date)
        raw_data = eval(self.get_html_str(url))
        try:
            open_info_raw = raw_data['data'][0]
            close_info_raw = raw_data['data'][-1]
        except KeyError:
            logging.error("No deal info. on %s" % date)
            return
        field = ['bid_deal', 'bid_volume', 'ask_deal', 'ask_volume', 'acc_deal', 'acc_volume', 'acc_value']
        offset = 1
        open_info = {}
        close_info = {}
        for i in range(len(field)):
            open_info[field[i]] = self.get_pure_float(open_info_raw[i+offset])
            close_info[field[i]] = self.get_pure_float(close_info_raw[i+offset])
        self.data[date]['open_deal'] = open_info
        self.data[date]['close_deal'] = close_info




    def format_url(self, date):
        _url = self.url + '?response=json&date=' + date
        #http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303
        return _url

    def format_url2(self, date):
        _url = self.url2 + 'date=' + date
        return _url
        #http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303



if __name__ == '__main__':
    ps = index_scrap(10)
    ps.set_data()

