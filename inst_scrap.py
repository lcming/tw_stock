#!/usr/bin/python3

from lxml import etree, html
from retry import retry
import urllib.request
import logging
from pprint import pprint as pp
import re
import datetime
from price_scrap import price_scrap
import sys

class inst_scrap(price_scrap):
    data_base_key = ['stock_id', 'name', 'foreign_buy', 'foreign_sell', 'foreign_diff', 'invest_buy', 'invest_sell', 'invest_diff', 'dealer_diff', 'dealer_buy_normal', 'dealer_sell_normal', 'dealer_diff_normal', 'dealer_buy_hedge', 'dealer_sell_hedge', 'dealer_diff_hedge', 'total_diff']

    def __init__(self, _stock_id, _trace_len):
        super().__init__(_stock_id, _trace_len)
        self.url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&'

    def format_url(self, date):
        _url = self.url + "date=" + date
        return _url
        # ex: http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201

    def get_stock_id_idx(self, stock_array, stock_id):
        idx = 0
        found = 0
        stock_id_field = 0
        for stock in stock_array:
            if (str(stock[stock_id_field]) == str(stock_id)):
                found = 1
                break
            else:
                idx += 1
        if(found == 0):
            logging.error("stock not found in %s" % stock_array)
            sys.exit(0)
        return idx


    #TODO: retry with differnt strategy based on "很抱歉，沒有符合條件的資料!" or "幕前人數過多"
    def set_daily_info(self, date):
        daily_info = {}
        url = self.format_url(date)
        try:
            raw_data = eval(self.get_html_str(url))
        except SyntaxError:
            self.set_daily_info(date)
            return
        stat = raw_data['stat']
        if ('data' in raw_data):
            data_part = raw_data['data']
            idx = self.get_stock_id_idx(data_part, self.stock_id)
            for i in range(2, len(self.data_base_key)):
                key_name = self.data_base_key[i]
                try:
                    daily_info[key_name] = self.get_pure_int(data_part[idx][i])
                except IndexError:
                    logging.error("Out bound: idx = %s, i = %d" % (idx, i))
                    pp(data_part)
                    sys.exit(0)
        elif (stat == '很抱歉，目前線上人數過多，請您稍候再試'):
            self.set_daily_info(date)
            return
        elif (stat == '很抱歉，沒有符合條件的資料!'):
            logging.info("No trade on %s" % date)
            daily_info = None
        else:
            logging.error("error fetching inst data with url %s" )

        self.data[date] = daily_info

