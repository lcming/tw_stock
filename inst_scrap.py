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
import csv

class inst_scrap(price_scrap):
    data_base_key = ['stock_id', 'name',
                     'foreign_buy', 'foreign_sell', 'foreign_diff',
                     'foreign_dealer_buy', 'foreign_dealer_sell', 'foreign_dealer_diff',
                     'invest_buy', 'invest_sell', 'invest_diff',
                     'dealer_diff',
                     'dealer_buy_normal', 'dealer_sell_normal', 'dealer_diff_normal', 'dealer_buy_hedge',
                     'dealer_sell_hedge', 'dealer_diff_hedge', 'total_diff']
    total_shares = {}

    def __init__(self, _stock_id, _trace_len):
        super().__init__(_stock_id, _trace_len)
        self.url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&'
        self.set_total_shares()

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
        if found == 0:
            logging.error("stock %s not found in %s" % (stock, stock_array))
            idx = -1
        return idx


    #TODO: retry with differnt strategy based on "很抱歉，沒有符合條件的資料!" or "幕前人數過多"
    def set_daily_info(self, date):
        daily_info = {}
        sgt_cache_name =  self.cache_dir + self.__class__.__name__ + date + ".txt"
        url = self.format_url(date)
        cache_web = self.load_cache_web(sgt_cache_name)
        if cache_web:
            raw_data = eval(cache_web)
        else:
            try:
                web_str = self.get_html_str(url)
                raw_data = eval(web_str)
            except SyntaxError:
                logging.debug("eval cache web syntax error, retry...")
                raw_data = None
        stat = raw_data['stat']
        if ('data' in raw_data):
            data_part = raw_data['data']
            idx = self.get_stock_id_idx(data_part, self.stock_id)
            for i in range(2, len(self.data_base_key)):
                key_name = self.data_base_key[i]
                try:
                    if idx != -1:
                        daily_info[key_name] = self.get_pure_int(data_part[idx][i])
                    else:
                        daily_info[key_name] = 0
                except IndexError:
                    logging.error("Out bound: idx = %s, i = %d" % (idx, i))
                    pp(data_part)
                    sys.exit(0)
            invest_diff_percent = self.cal_diff_percent(self.stock_id, daily_info['invest_diff'])
            daily_info['invest_diff_percent'] = invest_diff_percent
        elif (stat == '很抱歉，目前線上人數過多，請您稍候再試'):
            #self.inval_cache_web(sgt_cache_name)
            self.set_daily_info(date)
            return
        elif (stat == '很抱歉，沒有符合條件的資料!'):
            logging.info("No trade on %s" % date)
            daily_info = None
        else:
            print(stat)
            logging.error("error fetching inst data with url %s" % url)

        if cache_web is None:
            self.fill_cache_web(sgt_cache_name, web_str)
        self.data[date] = daily_info

    def set_total_shares(self):
        if len(self.total_shares) == 0:
            with open("stock_info.csv", encoding='utf-8', errors='ignore') as fh:
                rd = csv.reader(fh, delimiter=',')
                iter_rd = iter(rd)
                next(iter_rd)
                for row in iter_rd:
                    self.total_shares[str(row[1])] = float(row[15])/10.0

    def cal_diff_percent(self, stock_id, diff):
        try:
            ts = self.total_shares[stock_id]
            if ts == 0:
                return 0.0
            else:
                return diff/ts
        except KeyError:
            return 0.0


if __name__ == "__main__":
    ss = inst_scrap("1312", 1)
    ss.set_today(2018, 4, 19)
    ss.set_data()

