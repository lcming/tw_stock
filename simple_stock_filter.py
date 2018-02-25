from price_scrap import price_scrap
from dist_scrap import dist_scrap
from inst_scrap import inst_scrap
from stock_scrap import stock_scrap
from foreign_scrap import foreign_scrap
from close_scrap import close_scrap
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

    def __init__(self, volume_min = 100000, price_min = 5.0, price_max = 200.0, traced_weeks = 2):
        self.volume_min = volume_min
        self.price_min = price_min
        self.price_max = price_max
        self.traced_weeks = traced_weeks

    def run_viz(self, traced_weeks):
        pass

    def run_filter(self, p_inc, f_inc, b_inc, f_tshd, b_tshd):
        self.set_all_stock_list()
        self.volume_now()
        self.price_window_inc_below(p_inc)
        self.foreign_inc_over(f_tshd, f_inc)
        #def foreign_inc_over(self, target_percent, target_inc_percent):
        self.big_inc_over(14, b_tshd, b_inc)
        #def big_inc_over(self, level, target_percent, target_inc_percent):
        return self.stock_list

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


    def big_inc_over(self, level, target_percent, target_inc_percent):
        new_list = []
        weeks_traced = self.traced_weeks + 1
        for st in self.stock_list:
            ss = dist_scrap(str(st), weeks_traced)
            if(self.test_mode):
                ss.set_today(2018, 1, 5)
            ss.set_data()
            week = 0
            ok = 1
            prev_percent = None
            most_recent_percent = None
            for date in ss.record_dates:
                try:
                    percent = ss.data[date]['dist'][level]['percent']
                    if(prev_percent == None):
                        logging.debug("starting big owner percent %f" % percent)
                        most_recent_percent = percent
                        if(most_recent_percent < target_percent):
                            logging.info("%s is out on %s, %f < target: %f" %(st, date, most_recent_percent, target_percent))
                            ok = 0
                            break
                    elif(prev_percent < percent):
                        ok = 0
                        logging.info("%s is out on %s, %f -> %f" %(st, date, prev_percent, percent))
                        break
                    logging.info("%s on %s: %f" %(st, date, percent))
                    prev_percent = percent
                    week += 1
                except IndexError:
                    print("big_percent_list: %d" % week)
                    print(big_percent_list)
                    sys.exit(1)

            inc_percent = (most_recent_percent - percent) / percent * 100.0

            if(ok == 1 and inc_percent > target_inc_percent):
                logging.info("%s: pass with %f" % (st, inc_percent))
                new_list.append(st)
            else:
                logging.info("%s: out with %f" % (st, inc_percent))

        self.stock_list = new_list

    def sample_list(self, list_in, rate):
        list_out = []
        i = 0
        while(i < len(list_in)):
            list_out.append(list_in[i])
            i += rate
        return list_out

    def foreign_inc_over(self, target_percent, target_inc_percent):
        new_list = []
        days_traced = self.traced_weeks * 5 + 1
        for st in self.stock_list:
            ss = foreign_scrap(str(st), days_traced)
            if(self.test_mode):
                ss.set_today(2018, 1, 5)
            ss.set_data()
            foreign_percent_list = self.dict_to_list(ss.data, 1)
            ok = 1
            prev_percent = None
            most_recent_percent = None
            sample_dates = self.sample_list(ss.record_dates, 5)
            for date in sample_dates:
                try:
                    percent = ss.data[date]
                    if(prev_percent == None):
                        logging.debug("starting foreign percent %f" % percent)
                        most_recent_percent = percent
                        if(most_recent_percent < target_percent):
                            logging.info("%s is out on %s, %f < target: %f" %(st, date, most_recent_percent, target_percent))
                            ok = 0
                            break
                    elif(prev_percent < percent):
                        ok = 0
                        logging.info("%s is out on %s, %f -> %f" %(st, date, prev_percent, percent))
                        break
                    logging.info("%s on %s: %f" %(st, date, percent))
                    prev_percent = percent
                except IndexError:
                    ss.dbg()
                    print("foreign_percent_list:")
                    print(foreign_percent_list)
                    sys.exit(1)

            inc_percent = (most_recent_percent - percent) / percent * 100.0

            if(ok == 1 and inc_percent > target_inc_percent):
                logging.info("%s: pass with %f" % (st, inc_percent))
                new_list.append(st)
            else:
                logging.info("%s: out with %f" % (st, inc_percent))

        self.stock_list = new_list

    def volume_now(self):
        new_list = []
        for st in self.stock_list:
            ps = close_scrap(str(st), 1)
            if(self.test_mode):
                ps.set_today(2018, 1, 5)
            ps.set_data()
            recent_trade_day = None
            for i in reversed(sorted(ps.data)):
                if(ps.data[i]):
                    recent_trade_day = i
                    break
            if(recent_trade_day == None):
                logging.error("no valid trade day found for %s" % st)
                sys.exit(1)
            v = ps.data[recent_trade_day]['deal_shares']
            if(v >= self.min_volume):
                logging.debug("%s pass minimum volume" % st)
                new_list.append(st)
        self.stock_list = new_list


    def price_window_inc_below(self, target_inc_percent):
        new_list = []
        for st in self.stock_list:
            recent_trade_day = None
            first_trade_day = None
            days_traced = 5 * self.traced_weeks + 1
            ps = price_scrap(str(st), days_traced)
            if(self.test_mode):
                ps.set_today(2018, 1, 5)
            ps.set_data()
            price_now = ps.data[ps.record_dates[0]]
            price_before = ps.data[ps.record_dates[-1]]
            price_inc = (price_now - price_before) / price_before * 100
            if(price_now <= self.price_max and price_now >= self.price_min and price_inc < target_inc_percent):
                logging.debug("%s - %f $" %(st, price_now))
                new_list.append(st)
            else:
                logging.debug("%s is out - %f $" %(st, price_now))
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


if __name__ == "__main__":
    logging.basicConfig(filename='ssf.log', level=logging.DEBUG)
    for i in range(1, 1):

        volume_min = 100000
        price_min = 5.0
        price_max = 200.0
        traced_weeks = 2

        inc = i * 0.25
        b_inc = inc
        f_inc = inc * 0.5
        pri_i = inc
        f_tshd = 10.0
        b_tshd = 50.0

        ssf = simple_stock_filter(volume_min, price_min, price_max, traced_weeks)
        ssf.run_filter(pri_i, f_inc, b_inc, f_tshd, b_tshd)

        print("parameter = %d" % i)
        print(ssf.stock_list)

