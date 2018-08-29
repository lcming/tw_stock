#!/usr/bin/python3

from lxml import etree, html
import logging
import traceback
import pprint
import datetime
from stock_scrap import stock_scrap
from requests import Request, Session, exceptions
from retry import retry

class dist_scrap(stock_scrap):
    ranges = []
    valid_dates = []

    def __init__(self, _stock_id, _trace_len):
        _url = 'https://www.tdcc.com.tw/smWeb/QryStockAjax.do'
        super().__init__(_stock_id, _trace_len, _url)
        self.set_valid_dates()
        self.none_cnt = 0

    def get_min_max(self, share_range):
        import re
        pat = re.compile(',')
        share_range = pat.sub("", share_range)
        pat = re.compile('\d+')
        matched = pat.findall(share_range)
        if (len(matched) == 1):
            matched.append(None)
        return matched

    def parsePOSTstring(self, POSTstr):
        paramList = POSTstr.split('&')
        paramDict = dict([param.split('=') for param in paramList])
        return paramDict

    def set_valid_dates(self):
        while len(dist_scrap.valid_dates) == 0:
            logging.info("set valid dates for dist scrap")
            POSTstr = "REQ_OPR=qrySelScaDates"
            vd_str = self.get_ajax_str(POSTstr)
            dist_scrap.valid_dates = eval(vd_str)

    def get_html_str(self, date):
        POSTstr = "StockNo=" + self.stock_id + "&clkStockNo=" + self.stock_id + "&scaDate=" + date + "&StockName=&REQ_OPR=SELECT&clkStockName=&SqlMethod=StockNo"
        html_str = self.get_ajax_str(POSTstr)
        return html_str

    def get_ajax_str(self, POSTstr):
        import time
        time.sleep(5)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
                #'Referer' : 'https://www.tdcc.com.tw/smWeb/QryStockAjax.do'
                'Referer' : 'https://www.tdcc.com.tw/smWeb/QryStock.jsp'
                }
            payload = self.parsePOSTstring(POSTstr)
            s = Session()
            r = s.post(self.url, data = payload, headers=headers)
            logging.debug("Request %s" % self.url)
            ajax_str = r.text
            s.close()
        except exceptions.ConnectionError:
            s.close()
            ajax_str = self.get_ajax_str(POSTstr)
        return ajax_str

    def set_daily_info(self, date):
        if date not in self.valid_dates:
            self.data[date] = None
            return
        daily_info = {}
        day_dist = []
        max_level = 15
        cnt = 0
        html_str = self.get_html_str(date)
        root = etree.HTML(html_str)
        try:
            data_pos = 6
            table_rows = root.xpath("//form/table/tr/td/table[position()=%s]/tbody/tr[position()>1]" % str(data_pos))
            for row in table_rows:
                idx = row[0].text
                cnt += 1
                if (cnt <= max_level):
                    #share_range = row[1].text
                    data = {}
                    #data["min"], data["max"] = self.get_min_max(share_range)
                    data["owners"] = self.get_pure_int(row[2].text)
                    data["shares"] = self.get_pure_int(row[3].text)
                    data["percent"] = self.get_pure_float(row[4].text)
                    day_dist.append(data)
                elif (idx == '\xa0'):
                    total_owners = self.get_pure_int(row[2].text)
                    total_shares = self.get_pure_int(row[3].text)
                else:
                    logging.warn("warning: unrecognize pattern %s" % idx)
            daily_info["dist"] = day_dist
            daily_info["total_owners"] = total_owners
            daily_info["total_shares"] = total_shares
        except IndexError:
            logging.debug("Dump rows:")
            for col in row:
                logging.debug(col.text)
            logging.error(traceback.format_exc())
            logging.fatal("cannot parse the page %s" % html_str)

        if len(daily_info) == 0:
            if self.daily_failed_cnt < self.max_fail_cnt:
                self.daily_failed_cnt += 1
                self.set_daily_info(date)
                return
        self.data[date] = daily_info

    def format_url(self, date):
        _url = self.url + '?SCA_DATE=' + date + '&SqlMethod=StockNo&StockNo=' + str(self.stock_id) + '&StockName=&sub=%ACd%B8%DF'
        return _url

if __name__ == '__main__':
    ds = dist_scrap("3035", 1)
    ds.set_today(2017, 11, 24)
    ds.set_data()
    #ds = dist_scrap("3035", 21, url_base)
