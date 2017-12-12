#!/usr/bin/python3

from lxml import etree, html
from retry import retry
import urllib.request
import logging
import pprint
import re
import datetime
from price_scrap import price_scrap

class inst_scrap(price_scrap):
    data_base_key = ['stock_id', 'name', 'foreign_buy', 'foreign_sell', 'foreign_diff', 'invest_buy', 'invest_sell', 'invest_diff', 'dealer_diff', 'dealer_buy_normal', 'dealer_sell_normal', 'dealer_diff_normal', 'dealer_buy_hedge', 'dealer_sell_hedge', 'dealer_diff_hedge', 'total_diff']

    def __init__(self, _stock_id, _trace_len):
        super().__init__(_stock_id, _trace_len)
        self.url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&'

    def set_dates_list(self):
        days_traced = 0
        d = self.today
        while (days_traced < self.trace_len):
            self.request_dates.append(self.get_date_string(d))
            d -= datetime.timedelta(1)
            days_traced += 1


    def format_url(self, date):
        _url = self.url + "date=" + date
        return _url
        # ex: http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201

    def get_stock_id_idx(self, stock_array, stock_id):
        idx = 0
        stock_id_field = 0
        for stock in stock_array:
            if (stock[stock_id_field] == stock_id):
                break
            else:
                idx += 1
        return idx

    def set_data(self):
        self.set_dates_list()
        for date in self.request_dates:
            raw_data = eval(self.get_html_str(self.format_url(date)))
            if 'data' in raw_data:
                self.record_dates.append(date)
                data_part = raw_data['data']
                idx = self.get_stock_id_idx(data_part, self.stock_id)
                stock_info_today = {}
                for i in range(2, len(self.data_base_key)):
                    key_name = self.data_base_key[i]
                    stock_info_today[key_name] = self.get_pure_int(data_part[idx][i])
                self.data[date] = stock_info_today
            else:
                print("No trade on %s" % date)










