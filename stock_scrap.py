#!/usr/bin/python3
import datetime
import urllib.request
import ssl
from retry import retry
from pprint import pformat as pf
import logging
import os
import sys

class stock_scrap:
    stock_id = None
    url = None
    trace_len = None
    today = None
    record_dates = []
    cache_data = {}
    data = {}
    min_new_data_range = 0

    # dbg
    hit_count = 0

    def __init__(self, _stock_id, _trace_len, _url):
        self.today = datetime.date.today() - datetime.timedelta(1)
        self.stock_id = _stock_id
        self.trace_len = _trace_len
        self.url = _url
        self.record_dates.clear()
        self.data.clear()
        self.cache_name =  "./cache/" + self.__class__.__name__+ str(_stock_id) + ".txt"

    def get_date_string(self, d):
        y_str = d.year
        m_str = str(0) + str(d.month) if len(str(d.month)) == 1 else str(d.month)
        d_str = str(0) + str(d.day) if len(str(d.day)) == 1 else str(d.day)
        return "%s%s%s" % (y_str, m_str, d_str)

    def set_today(self, y, m, d):
        new_date = datetime.date(y, m, d)
        self.today = new_date

    def dbg(self):
        logging.debug("DEBUG stock_scrap")
        logging.debug("Stock: %s, url: %s, today: %s" % (self.stock_id, self.url, self.today))
        logging.debug("Record dates include:"),
        logging.debug(pf(self.record_dates))
        logging.debug("Record dates include:"),
        logging.debug(pf(self.data))

    def set_daily_info(self, date):
        assert(False)

    def format_url(self, date):
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



    #@retry(urllib.error.URLError)
    def get_html_str(self, url):
        import time
        try:
            time.sleep(2)
            req = urllib.request.Request(url, headers = {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
            logging.debug(url)
            rsp = urllib.request.urlopen(req)
            read_data = rsp.read()
            html_str = read_data.decode('utf8')
            time.sleep(2)
        except UnicodeDecodeError:
            html_str = read_data.decode('big5')
        except (urllib.error.URLError, ssl.SSLError) as e:
            html_str = self.get_html_str(url)
        return html_str

    def load_cache_web(self, fname, url):
        try:
            with open(fname, 'r', encoding='utf-8') as infile:
                cache_web = infile.read()
                infile.close()
                logging.info("web cache %s hit" % fname)
        except (FileNotFoundError) as e:
            logging.info("web cache %s miss, request URL" % fname)
            try:
                cache_web = self.get_html_str(url)
                self.fill_cache_web(fname, cache_web)
            except SyntaxError:
                cache_web = self.load_cache_web(date, url)
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
        new_data_range = 0

        while (days_traced < self.trace_len):
            date = self.get_date_string(d)
            if(date in self.data and new_data_range >= self.min_new_data_range):
                self.hit_count += 1
                if(self.data[date]):
                    days_traced += 1
            else:
                logging.info("Cache miss on %s" % date)
                self.set_daily_info(date)
                new_data_range += 1
                try:
                    if(self.data[date]):
                        self.record_dates.append(date)
                        days_traced += 1
                except KeyError:
                    self.data[date] = None
            d -= datetime.timedelta(1)

        self.store_cache_data()







