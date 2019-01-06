#!/usr/bin/python3

from lxml import etree, html
import logging
import pprint
import re
import datetime
from op_scrap import op_scrap
from index_scrap import *

class op_close_scrap(op_scrap):

    def __init__(self, _trace_len):
        super().__init__(_trace_len)
        self.url = 'http://www.taifex.com.tw/cht/3/dlOptDataDown?down_type=1&commodity_id=TXO&commodity_id2=&'

    def inc_target_month(self, tm):
        year = tm[0:4]
        mon = tm[4:6]
        if int(mon) == 12:
            mon = "01"
            year = str(int(year)+1)
        elif int(mon) < 9:
            mon = "0" + str(int(mon[1])+1)
        else:
            mon = str(int(mon)+1)
        return year+mon

    def parse_op_csv(self, csv_str, date):
        rows = csv_str.split("\n")
        if len(rows) < 3:
            return None
        target_month = self.get_target_month(date)
        target_week = target_month + "W"
        target_month_idx = 2
        target_week_idx = 2
        week_ref_price, month_ref_price = self.get_ref_price(date)
        data = {}
        data["week"] = {}
        data["month"] = {}
        data["week"]["price"] = week_ref_price
        data["month"]["price"] = month_ref_price
        ref_price_idx = 3
        close_price_idx = 8
        deal_type_idx = 4
        deal_time_idx = 17
        week_hit = 0
        for row in rows:
            entry = row.split(",")
            if len(entry) < 19:
                continue
            ref_price = int(float(entry[ref_price_idx].strip()))
            deal_type = entry[deal_type_idx].strip()
            deal_time = entry[deal_time_idx].strip()
            if ref_price == week_ref_price and deal_time == '一般' and deal_type == '買權' and week_hit < 2:
                data["week"]["c"] = entry[close_price_idx]
                week_hit += 1
            if ref_price == week_ref_price and deal_time == '一般' and deal_type == '賣權' and week_hit < 2:
                data["week"]["p"] = entry[close_price_idx]
                week_hit += 1

            if ref_price == month_ref_price and deal_time == '一般' and deal_type == '買權' and week_hit >= 2:
                data["month"]["c"] = entry[close_price_idx]
                week_hit += 1
            if ref_price == month_ref_price and deal_time == '一般' and deal_type == '賣權' and week_hit >= 2:
                data["month"]["p"] = entry[close_price_idx]
                week_hit += 1
            if week_hit == 4:
                break
            if "c" not in data["month"]:
                data["month"]["c"] = "nan"
            if "p" not in data["month"]:
                data["month"]["p"] = "nan"
            if "c" not in data["week"]:
                data["week"]["c"] = "nan"
            if "p" not in data["week"]:
                data["week"]["p"] = "nan"
        return data

    def get_ref_price(self, date):
        data = eval(open("cache/index_scrap_tw_index.txt", "r").read())
        close = int(data[date]['close'])
        month_unit = 100
        if close > 10000.0:
            week_unit = 100
        else:
            week_unit = 50
        month_residual = close % month_unit
        week_residual = close % week_unit
        if month_residual >= month_unit/2:
            month_carry = 1
        else:
            month_carry = 0
        if week_residual >= week_unit/2:
            week_carry = 1
        else:
            week_carry = 0
        if month_carry:
            ref_month = close - month_residual + month_unit
        else:
            ref_month = close - month_residual
        if week_carry:
            ref_week = close - week_residual + week_unit
        else:
            ref_week = close - week_residual
        return int(ref_week), int(ref_month)

    def get_target_month(self, date):
        year = date[0:4]
        month = date[4:6]
        return year+month

    def set_daily_info(self, date):
        url = self.format_url(date)
        html_str = self.get_html_str(url)
        try:
            self.data[date] = self.parse_op_csv(html_str, date)
        except Exception as e:
            print(str(e))
            self.data[date] = "ERROR"
            #import sys
            #sys.exit(1)

    def format_url(self, date):
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        #queryDate=2018%2F03%2F20
        _url = self.url + "queryStartDate=" + year + "%2F" + month + "%2F" + day
        _url += "&"     + "queryEndDate="  + year + "%2F" + month + "%2F" + day
        return _url


if __name__ == '__main__':
    #fs = index_scrap(200)
    #fs.set_data()
    log_name = 'ssf.log'
    logging.basicConfig(filename='ssf.log', level=logging.DEBUG)
    fs = op_close_scrap(600)
    fs.set_stop_date("20170101")
    fs.set_data()
    #path = "sample.csv"
    #path = "error.log"
    #with open(path, 'r', encoding='big5') as f:
    #    csv_str = f.read()
    #print(fs.parse_op_csv(csv_str, "20180320"))
    #print(fs.get_ref_price("20180119"))
    #url = fs.format_url("20180320")
    #html_str = fs.get_html_str(url)
    #print(html_str)

