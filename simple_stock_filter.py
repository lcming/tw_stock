from price_scrap import price_scrap
from dist_scrap import dist_scrap
from inst_scrap import inst_scrap
from stock_scrap import stock_scrap
from foreign_scrap import foreign_scrap
from pprint import pformat as pf
import datetime
import collections
import numpy as np
import logging
import re
import urllib.request
import sys


class simple_stock_filter:

    # dbg
    y = 2018
    m = 1
    d = 6
    test_mode = 0
    stock_list = []

    def run_filter(self):
        self.stock_list = self.get_all_stock_list()
        self.price_now(price_max, price_min)
        #self.foreign_percent(inc_weeks, inc_percent)
        #self.big_owner_percent(inc_weeks, inc_percent)
        return stock_list

    def dict_to_list(self, dict_in, reverse):
        ret_list = []
        if(reverse == 1):
            for i in reversed(sorted(dict_in)):
                if(dict_in[i]):
                    ret_list.append(dict_in[i])
        else:
            for i in sorted(dict_in):
                if(dict_in[i]):
                    ret_list.append(dict_in[i])
        return ret_list

    def dict_list_item_to_list(self, dict_in, reverse, idx):
        ret_list = []
        if(reverse == 1):
            for i in reversed(sorted(dict_in)):
                if(dict_in[i]):
                    ret_list.append(dict_in[i]['dist'][idx]['percent'])
        else:
            for i in sorted(dict_in):
                if(dict_in[i]):
                    ret_list.append(dict_in[i]['dist'][idx]['percent'])
        return ret_list


    def big_owner_percent(self, level, target_percent, inc_weeks, target_inc_percent):
        new_list = []
        for st in self.stock_list:
            ss = dist_scrap(str(st), inc_weeks + 1)
            if(self.test_mode):
                ss.set_today(2018, 1, 5)
            ss.set_data()
            big_percent_list = self.dict_list_item_to_list(ss.data, 1, level)
            week = 0
            ok = 1
            prev_percent = None
            most_recent_percent = None
            while(week < inc_weeks):
                try:
                    percent = big_percent_list[week]
                    if(prev_percent == None):
                        logging.debug("starting big owner percent %f" % percent)
                        most_recent_percent = percent
                        if(most_recent_percent < target_percent):
                            logging.info("%s is out, %f < target: %f" %(st, most_recent_percent, target_percent))
                            ok = 0
                            break
                    elif(prev_percent < percent):
                        ok = 0
                        logging.info("%s is out, %f -> %f" %(st, prev_percent, percent))
                        break
                    logging.info("%s: %f" %(st, percent))
                    prev_percent = percent
                    week += 1
                except IndexError:
                    print("big_percent_list: %d" % week)
                    print(big_percent_list)
                    sys.exit(1)

            inc_percent = (most_recent_percent - percent) / percent

            if(ok == 1 and inc_percent > target_inc_percent):
                logging.info("%s: pass" % st)
                new_list.append(st)

        self.stock_list = new_list


    def foreign_percent(self, target_percent, inc_weeks, target_inc_percent):
        new_list = []
        days_traced = inc_weeks * 5 + 1
        for st in self.stock_list:
            ss = foreign_scrap(str(st), days_traced)
            if(self.test_mode):
                ss.set_today(2018, 1, 5)
            ss.set_data()
            foreign_percent_list = self.dict_to_list(ss.data, 1)
            day = 0
            ok = 1
            prev_percent = None
            most_recent_percent = None
            while(day < days_traced):
                try:
                    percent = foreign_percent_list[day]
                    if(prev_percent == None):
                        logging.debug("starting foreign percent %f" % percent)
                        most_recent_percent = percent
                        if(most_recent_percent < target_percent):
                            logging.info("%s is out, %f < target: %f" %(st, most_recent_percent, target_percent))
                            ok = 0
                            break
                    elif(prev_percent < percent):
                        ok = 0
                        logging.info("%s is out, %f -> %f" %(st, prev_percent, percent))
                        break
                    logging.info("%s: %f" %(st, percent))
                    prev_percent = percent
                    day += 5
                except IndexError:
                    ss.dbg()
                    print("foreign_percent_list:")
                    print(foreign_percent_list)
                    sys.exit(1)



            inc_percent = (most_recent_percent - percent) / percent

            if(ok == 1 and inc_percent > target_inc_percent):
                logging.info("%s: pass" % st)
                new_list.append(st)

        self.stock_list = new_list

    def price_now(self, price_max, price_min, inc_weeks, target_inc_percent):
        new_list = []
        for st in self.stock_list:
            recent_trade_day = None
            first_trade_day = None
            days_traced = 5 * inc_weeks + 1
            ps = price_scrap(str(st), days_traced)
            if(self.test_mode):
                ps.set_today(2018, 1, 5)
            ps.set_data()
            for i in reversed(sorted(ps.data)):
                if(ps.data[i]):
                    recent_trade_day = i
                    break
            for i in sorted(ps.data):
                if(ps.data[i]):
                    first_trade_day = i
                    break
            price_now = ps.data[recent_trade_day]
            price_before = ps.data[first_trade_day]
            price_inc = (price_now - price_before) / price_before
            if(price_now <= price_max and price_now >= price_min and price_inc < target_inc_percent):
                logging.debug("%s - %f $" %(st, price_now))
                new_list.append(st)
        self.stock_list = new_list

    def set_all_stock_list(self):
        ss = stock_scrap("", "", "")
        url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201'
        data_part = None
        while(data_part is None):
            try:
                html_str = ss.get_html_str(url)
                raw_data = eval(html_str)
                data_part = raw_data['data']
            except KeyError:
                logging.info("retry...")
                pass
        all_stock_list = []
        for stock in  data_part:
            stock_id = stock[0]
            pat = re.compile('^[1-9]\d{3}$')
            if(pat.match(stock_id)):
                all_stock_list.append(stock_id)
        logging.debug("all_stock_list: %s" % str(all_stock_list))
        self.stock_list = all_stock_list


