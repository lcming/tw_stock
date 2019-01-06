#!/usr/bin/python3

from lxml import etree, html
import logging
import pprint
import re
import datetime
from stock_scrap import stock_scrap

class jur_scrap(stock_scrap):

    def __init__(self, _trace_len):
        _url = 'http://www.twse.com.tw/fund/BFI82U?response=json&type=day&dayDate='
        super().__init__("_tw_index", _trace_len, _url)

    def set_daily_info(self, date):
        daily_info = {}
        day_dist = []
        url = self.format_url(date)
        html_str = self.get_html_str(url)
        null = None
        raw_data = eval(html_str)
        diff_idx = 3
        label = ["dealer", "dealer_hedge", "inst", "foreign", "foreign_dealer", "overall"]
        if "data" in raw_data:
            for l, d in zip(label, raw_data["data"]):
                daily_info[l] = self.get_pure_int(d[diff_idx])
        else:
            daily_info = None
        self.data[date] = daily_info

    def format_url(self, date):
        #queryDate=2018%2F03%2F20
        _url = self.url + date
        return _url

if __name__ == '__main__':
    js = jur_scrap(200)
    js.set_data()

