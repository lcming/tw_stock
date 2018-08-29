#!/usr/bin/python3

from lxml import etree, html
import urllib.request
import logging
from pprint import pprint as pp
import re
import datetime
from stock_scrap import stock_scrap
import sys
import csv

class inst_scrap(stock_scrap):
    data_base_key = ['stock_id', 'name',
                     'foreign_buy', 'foreign_sell', 'foreign_diff',
                     'foreign_dealer_buy', 'foreign_dealer_sell', 'foreign_dealer_diff',
                     'invest_buy', 'invest_sell', 'invest_diff',
                     'dealer_diff',
                     'dealer_buy_normal', 'dealer_sell_normal', 'dealer_diff_normal', 'dealer_buy_hedge',
                     'dealer_sell_hedge', 'dealer_diff_hedge', 'total_diff']
    total_shares = {}

    def __init__(self, _stock_id, _trace_len):
        url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&'
        super().__init__(_stock_id, _trace_len, url)
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

    def parse_total_stock_daily_info(self, raw_data):
        daily_info = {}
        ok = 0
        if 'data' in raw_data:
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
            ok = 1
        return daily_info, ok

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

