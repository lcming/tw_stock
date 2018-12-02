#!/usr/bin/python3

from lxml import etree, html
import logging
import pprint
import re
import datetime
from stock_scrap import stock_scrap

class op_scrap(stock_scrap):

    def __init__(self, _trace_len):
        _url = 'http://www.taifex.com.tw/cht/3/callsAndPutsDate?queryType=1&goDay=&doQuery=1&dateaddcnt=&'
        super().__init__("_tw_index", _trace_len, _url)
        self.url2 = "http://www.twse.com.tw/exchangeReport/MI_5MINS?"

    def get_last_day_of_prev_month(self, d):
        old_d = d
        while (d.month == old_d.month):
            d -= datetime.timedelta(1)
        return d

    def set_daily_info(self, date):
        daily_info = {}
        day_dist = []
        url = self.format_url(date)
        html_str = self.get_html_str(url)
        root = etree.HTML(html_str)
        try:
            daily_info['dealer call'] = self.parse_op_table(root, 4, 4, 16)
            daily_info['inst call'] = self.parse_op_table(root, 5, 1, 13)
            daily_info['foreign call'] = self.parse_op_table(root, 6, 1, 13)
            daily_info['dealer put'] = self.parse_op_table(root, 7, 2, 14)
            daily_info['inst put'] = self.parse_op_table(root, 8, 1, 13)
            daily_info['foreign put'] = self.parse_op_table(root, 9, 1, 13)
        except Exception as e:
            print(e)
            daily_info = None
        print(date)
        print(daily_info)
        self.data[date] = daily_info

    def parse_op_table(self, root, row, col_start, col_end):
        tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(row))
        data = []
        for i in range(col_start, col_end):
            value = tds[i].text
            if value is None or len(value.strip()) == 0:
                if tds[i].find('font') is None:
                    value = tds[i].findall('div')[1].text
                else:
                    value = tds[i].find('font').text
            data_strip = value.strip()
            data.append(self.get_pure_int(data_strip))
        return data

    def format_date(self, date):
        # from 106/11/11 to 20171111
        y, m, d = date.split('/')
        y = int(y) + 1911
        return str(y) + str(m) + str(d)

    def format_url(self, date):
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        #queryDate=2018%2F03%2F20
        _url = self.url + "queryDate=" + year + "%2F" + month + "%2F" + day
        return _url


if __name__ == '__main__':
    os = op_scrap(300)
    os.set_data()

