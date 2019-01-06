#!/usr/bin/python3

from lxml import etree, html
import logging
import pprint
import re
import datetime
from op_scrap import op_scrap

class fu_scrap(op_scrap):

    def __init__(self, _trace_len):
        super().__init__(_trace_len)
        self.url =  'http://www.taifex.com.tw/cht/3/futContractsDate?queryType=1&goDay=&doQuery=1&dateaddcnt=&'
        self.url2 = 'http://www.taifex.com.tw/cht/3/futDailyMarketReport?queryType=2&marketCode=0&commodity_id=TX&'

    def set_daily_info(self, date):
        daily_info = {}
        day_dist = []
        url, url2 = self.format_url(date)
        html_str = self.get_html_str(url)
        root = etree.HTML(html_str)
        try:
            daily_info['dealer'] = self.parse_fu_table(root, 4, 3, 15)
            daily_info['inst'] = self.parse_fu_table(root, 5, 1, 13)
            daily_info['foreign'] = self.parse_fu_table(root, 6, 1, 13)
        except Exception as e:
            print(e)
            self.data[date] = None
            return
        # today is valid, then do second part
        html_str = self.get_html_str(url2)
        root = etree.HTML(html_str)
        try:
            daily_info['price'] = self.parse_fu_table2(root, 2, 6)
        except Exception as e:
            print(e)
        print(date)
        print(daily_info)
        self.data[date] = daily_info

    def format_url(self, date):
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        #queryDate=2018%2F03%2F20
        #_url = self.url + "queryStartDate=" + year + "%2F" + month + "%2F" + day
        #_url += "&"     + "queryEndDate="  + year + "%2F" + month + "%2F" + day

        _url  = self.url  + "queryDate=" + year + "%2F" + month + "%2F" + day
        _url2 = self.url2 + "queryDate=" + year + "%2F" + month + "%2F" + day
        return _url, _url2

    def parse_fu_table(self, root, row, col_start, col_end):
        tds = root.xpath("//tr/td/table/tbody/tr[position()=%s]/td" % str(row))
        data = []
        for i in range(col_start, col_end):
            if len(tds[i].xpath("div/font")) > 0:
                value = tds[i].xpath("div/font")[0].text
            elif len(tds[i].xpath("div")) > 0:
                value = tds[i].xpath("div")[0].text
            data_strip = value.strip()
            data.append(self.get_pure_int(data_strip))
        return data

    def parse_fu_table2(self, root, row_start, row_end):
        tds = root.xpath('//*[@id="printhere"]/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td')
        data = []
        for i in range(row_start, row_end):
            data.append(self.get_pure_int(tds[i].text.strip()))
        return data


if __name__ == '__main__':
    #html_str = open("error.html", "r").read()
    #root = etree.HTML(html_str)
    #print(fs.parse_fu_table(root, 4, 3, 15))
    #print(fs.parse_fu_table(root, 5, 1, 13))
    #print(fs.parse_fu_table(root, 6, 1, 13))
    log_name = 'ssf.log'
    logging.basicConfig(filename='ssf.log', level=logging.DEBUG)
    fs = fu_scrap(300)
    fs.set_data()
