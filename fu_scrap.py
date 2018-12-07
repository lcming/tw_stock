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
        self.url = 'https://www.taifex.com.tw/cht/3/futContractsDate?'

    def set_daily_info(self, date):
        daily_info = {}
        day_dist = []
        url = self.format_url(date)
        html_str = self.get_html_str(url)
        root = etree.HTML(html_str)
        try:
            daily_info['dealer'] = self.parse_fu_table(root, 4, 3, 15)
            daily_info['inst'] = self.parse_fu_table(root, 5, 1, 13)
            daily_info['foreign'] = self.parse_fu_table(root, 6, 1, 13)
        except Exception as e:
            print(e)
            daily_info = None
        print(date)
        print(daily_info)
        self.data[date] = daily_info

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


if __name__ == '__main__':
    #html_str = open("error.html", "r").read()
    #root = etree.HTML(html_str)
    fs = fu_scrap(300)
    #print(fs.parse_fu_table(root, 4, 3, 15))
    #print(fs.parse_fu_table(root, 5, 1, 13))
    #print(fs.parse_fu_table(root, 6, 1, 13))
    fs.set_data()

