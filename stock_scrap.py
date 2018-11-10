#!/usr/bin/python3
import datetime
import urllib.request
import ssl
from retry import retry
from pprint import pformat as pf
import logging
import os
import sys

class foo:
    pass

class StockTraceException(Exception):
    pass

class stock_scrap:
    trace_bound = "20180101"
    stock_id = None
    url = None
    trace_len = None
    today = None
    record_dates = []
    cache_data = {}
    data = {}

    # dbg
    scratch_mode = 0

    def __init__(self, _stock_id, _trace_len, _url):
        self.today = self._get_today()
        self.stock_id = _stock_id
        self.trace_len = _trace_len
        self.url = _url
        self.record_dates.clear()
        self.data.clear()
        self.max_fail_cnt = 5
        if self.scratch_mode == 1:
            self.cache_dir = "./cache_scratch/"
        else:
            self.cache_dir = "./cache/"
        self.cache_name = self.cache_dir + self.__class__.__name__+ str(_stock_id) + ".txt"

    def _get_today(self):
        if int(datetime.datetime.now().hour) < 19:
            return datetime.date.today() - datetime.timedelta(1)
        else:
            return datetime.date.today()

    def get_date_string(self, d):
        y_str = d.year
        m_str = str(0) + str(d.month) if len(str(d.month)) == 1 else str(d.month)
        d_str = str(0) + str(d.day) if len(str(d.day)) == 1 else str(d.day)
        return "%s%s%s" % (y_str, m_str, d_str)

    def set_today(self, y=None, m=None, d=None):
        if y is None or m is None or d is None:
            self.today = datetime.date.today()
        else:
            new_date = datetime.date(y, m, d)
            self.today = new_date

    def dbg(self):
        logging.debug("DEBUG stock_scrap")
        logging.debug("Stock: %s, url: %s, today: %s" % (self.stock_id, self.url, self.today))
        logging.debug("Record dates include:"),
        logging.debug(pf(self.record_dates))
        logging.debug("Record dates include:"),
        logging.debug(pf(self.data))

    def format_url(self, date):
        assert(False)

    def parse_total_stock_daily_info(self, raw_data):
        assert(False)

    def get_pure_int(self, number):
        import re
        number_old = number
        try:
            number = str(number)
            pat = re.compile('^\s*-')
            negtive = pat.match(number)
            pat = re.compile('\..*')
            number = pat.sub("", number)
            pat = re.compile('\D')
            number = pat.sub("", number)
            if(negtive):
                return -int(number)
            else:
                return int(number)
        except:
            logging.warn("failed converting int %s" % number_old)
            return None

    def get_pure_float(self, number):
        import re
        number_old = number
        try:
            number = str(number)
            pat = re.compile('((?=[^\.])\D)')
            number = pat.sub("", number)
            return float(number)
        except:
            logging.error("failed converting float %s" % number_old)
            return None

    def get_html_str(self, url):
        import time
        try:
            time.sleep(5)
            req = urllib.request.Request(url, headers = {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
            logging.debug("requested URL:")
            logging.debug(url)
            rsp = urllib.request.urlopen(req)
            read_data = rsp.read()
            html_str = read_data.decode('utf8')
        except UnicodeDecodeError:
            html_str = read_data.decode('big5')
        except (urllib.error.URLError, ssl.SSLError) as e:
            html_str = self.get_html_str(url)
        return html_str

    def load_cache_web(self, fname):
        try:
            with open(fname, 'r', encoding='utf-8') as infile:
                cache_web = infile.read()
                infile.close()
                logging.info("web cache %s hit" % fname)
        except (FileNotFoundError) as e:
            logging.info("web cache %s miss, request URL" % fname)
            return None
        return cache_web

    def fill_cache_web(self, fname, cache_web):
        with open(fname, 'w', encoding='utf-8') as outfile:
            logging.info("store cache web")
            outfile.write(str(cache_web))
            outfile.close()

    def inval_cache_web(self, fname):
        os.remove(fname)

    def load_cache_data(self):
        try:
            with open(self.cache_name, 'r', encoding='utf-8') as infile:
                cache_str = infile.read()
                self.data = eval(cache_str)
                logging.debug("load cache data")
                infile.close()
        except (FileNotFoundError, SyntaxError) as e:
            logging.info("Initialize cache %s" % self.cache_name)
            with open(self.cache_name, 'w', encoding='utf-8') as outfile:
                outfile.close()
            return

    def store_cache_data(self):
        with open(self.cache_name, 'w', encoding='utf-8') as outfile:
            logging.info("store cache data")
            outfile.write(str(self.data))
            outfile.close()

    def set_data(self):
        days_traced = 0
        d = self.today

        self.load_cache_data()
        self.set_data_failed = False

        try:
            b2b_no_trade = 0
            max_b2b_no_trade = 30
            while (days_traced < self.trace_len):
                date = self.get_date_string(d)
                if(date in self.data):
                    if(self.data[date]):
                        self.record_dates.append(date)
                        days_traced += 1
                        b2b_no_trade = 0
                else:
                    logging.info("%s Cache miss on %s" % (self.stock_id, date))
                    self.daily_failed_cnt =0
                    self.set_daily_info(date)
                    if date in self.data and self.data[date]:
                        self.record_dates.append(date)
                        days_traced += 1
                        b2b_no_trade = 0
                    else:
                        self.data[date] = None
                        b2b_no_trade += 1
                        if b2b_no_trade > max_b2b_no_trade:
                            logging.info("give up %s" % self.stock_id)
                            self.set_data_failed = True
                            break
                d -= datetime.timedelta(1)
        except OverflowError:
            logging.error("overflow in %s" % self.stock_id)
        self.store_cache_data()

    def set_daily_info(self, date):
        if int(date) < int(type(self).trace_bound):
            logging.error("Exceed bound %s" % self.stock_id)
            raise StockTraceException("Exceed bound!")
        sgt_cache_name =  self.cache_dir + self.__class__.__name__ + date + ".txt"
        url = self.format_url(date)
        cache_web = self.load_cache_web(sgt_cache_name)
        null = None
        if cache_web:
            raw_data = eval(cache_web)
        else:
            try:
                web_str = self.get_html_str(url)
                raw_data = eval(web_str)
            except SyntaxError:
                logging.debug("eval cache web syntax error, retry...")
                raw_data = None
        try:
            (daily_info, ok) = self.parse_total_stock_daily_info(raw_data)
        except TypeError:
            print("%s type error" % date)
            #print(raw_data)
            #print(daily_info)
        if ok:
            logging.info("ok")
        elif cache_web is None and self.daily_failed_cnt < self.max_fail_cnt:
            # we don't trust result from internet, so retry
            logging.info("retry %d times: %s" % (self.daily_failed_cnt, url))
            self.daily_failed_cnt += 1
            self.set_daily_info(date)
            return
        else:
            self.daily_failed_cnt = 0
            logging.info("No trade on %s" % date)
            daily_info = None

        if cache_web is None:
            self.fill_cache_web(sgt_cache_name, web_str)
        self.data[date] = daily_info







