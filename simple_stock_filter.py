# -*- coding: utf-8 -*-
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
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']



class simple_stock_filter:

    # dbg
    test_mode = 0
    stock_list = []
    black_list = ['9136']

    def __init__(self, volume_min = 100000, price_min = 5.0, price_max = 200.0, traced_weeks = 2):
        self.volume_min = volume_min
        self.price_min = price_min
        self.price_max = price_max
        self.traced_weeks = traced_weeks
        self.name_table = {}

    def get_foreign_inc(self, stock):
        days_traced = self.traced_weeks * 5 + 1
        ss = foreign_scrap(str(stock), days_traced)
        if(self.test_mode):
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if(len(ss.record_dates) > 0):
            sample_dates = self.sample_list(ss.record_dates, 5)
            start_date = sample_dates[-1]
            end_date = sample_dates[0]
            inc = ss.data[end_date] - ss.data[start_date]
            return inc
        else:
            logging.warn("No valid foreign data for %s" % stock)
            return 0.0

    def get_price_inc(self, stock):
        days_traced = self.traced_weeks * 5 + 1
        ss = price_scrap(str(stock), days_traced)
        if(self.test_mode):
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if(len(ss.record_dates) > 0):
            sample_dates = self.sample_list(ss.record_dates, 5)
            start_date = sample_dates[-1]
            end_date = sample_dates[0]
            inc = (ss.data[end_date] - ss.data[start_date]) / ss.data[start_date]
            return inc*100.0
        else:
            logging.warn("No valid price data for %s" % stock)
            return 0.0


    def get_big_level(self, stock):
        level = 14
        return level

    def get_big_inc(self, stock):
        level = self.get_big_level(stock)
        weeks_traced = self.traced_weeks + 1
        ss = dist_scrap(str(stock), weeks_traced)
        if(self.test_mode):
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if(len(ss.record_dates) > 0):
            start_date = ss.record_dates[-1]
            end_date = ss.record_dates[0]
            inc = (ss.data[end_date]['dist'][level]['percent'] - ss.data[start_date]['dist'][level]['percent'])
            return inc
        else:
            logging.warn("No valid big owner data for %s" % stock)
            return 0.0

    def update_bound(self, f_inc, b_inc, max_f, min_f, max_b, min_b):
        if(f_inc > max_f):
            max_f = f_inc
        if(f_inc < min_f):
            min_f = f_inc
        if(b_inc > max_b):
            max_b = b_inc
        if(b_inc < min_b):
            min_b = b_inc
        return (max_f, min_f, max_b, min_b)

    def get_plot_color(self, p_inc):
        if(p_inc > 0):
            if(p_inc > 10.0):
                p_inc = 10.0
            r, g, b= p_inc / 10.0, 0, 0
        elif(p_inc <= 0):
            if(p_inc < -10.0):
                p_inc = -10.0
            r, g, b = 0, -(p_inc / 10.0), 0
        else:
            r, g, b = 0, 0, 0

        return (r, g, b)

    def get_plot_text(self, stock, p_inc):
        name = stock
        sign = '+'
        if(self.name_table[stock]):
            name = self.name_table[stock]
        if(p_inc < .0):
            sign = ''
        text = name #+ sign + "{:.1f}".format(p_inc)
        return text

    def run_viz(self):
        self.set_all_stock_list()
        today_str = str(datetime.date.today())
        if(self.test_mode):
            self.stock_list = ['2330', '2317', '2303']
        self.volume_over()
        max_b = float("-inf")
        max_f = float("-inf")
        min_b = float("inf")
        min_f = float("inf")
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus']=False
        fig, ax = plt.subplots()
        fig.set_size_inches(20, 15, forward = True)
        plt.title("近%d週外資大戶持股與股價變化(製表日:%s)" % (self.traced_weeks, today_str))
        plt.xlabel("外資持股變化(%)")
        plt.ylabel("千張大戶持股變化(%)")
        for stock in self.stock_list:
            p_inc = self.get_price_inc(stock)
            f_inc = self.get_foreign_inc(stock)
            b_inc = self.get_big_inc(stock)
            max_f, min_f, max_b, min_b = self.update_bound(f_inc, b_inc, max_f, min_f, max_b, min_b)
            r, g, b = self.get_plot_color(p_inc)
            plot_text = self.get_plot_text(stock, p_inc)
            plt.text(f_inc, b_inc, plot_text, fontsize=8, color=(r, g, b))
            print(plot_text)
            print("%s: %f, %f, %f" % (stock, f_inc, b_inc, p_inc))

        plt.axis([max_f, min_f, max_b, min_b])
        plt.savefig("%s 近%d週變化.pdf" % (today_str, self.traced_weeks), dpi=300)



    def run_filter(self, p_inc, f_inc, b_inc, f_tshd, b_tshd):
        self.set_all_stock_list()
        self.volume_over()
        self.price_window_inc_below(p_inc)
        self.foreign_inc_over(f_tshd, f_inc)
        #def foreign_inc_over(self, target_percent, target_inc_percent):
        self.big_inc_over(14, b_tshd, b_inc)
        #def big_inc_over(self, level, target_percent, target_inc_percent):
        return self.stock_list

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
                    sys.exit(1)

            inc_percent = (most_recent_percent - percent) / percent * 100.0

            if(ok == 1 and inc_percent > target_inc_percent):
                logging.info("%s: pass with %f" % (st, inc_percent))
                new_list.append(st)
            else:
                logging.info("%s: out with %f" % (st, inc_percent))

        self.stock_list = new_list

    def volume_over(self):
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
            if(v >= self.volume_min):
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
            stock_name = stock[1]
            pat = re.compile('^[1-9]\d{3}$')
            if(pat.match(stock_id)):
                all_stock_list.append(stock_id)
                self.name_table[stock_id] = stock_name.strip()
        logging.debug("all_stock_list: %s" % str(all_stock_list))
        for st in self.black_list:
            all_stock_list.remove(st)
        self.stock_list = all_stock_list


if __name__ == "__main__":
    logging.basicConfig(filename='ssf.log', level=logging.DEBUG)
    volume_min = 100000
    price_min = 5.0
    price_max = 200.0
    for i in range(1):
        traced_weeks = i + 1
        ssf = simple_stock_filter(volume_min, price_min, price_max, traced_weeks)
        ssf.run_viz()
    #for i in range(1, 11):

    #    volume_min = 100000
    #    price_min = 5.0
    #    price_max = 4000
    #    traced_weeks = 2

    #    inc = i * 0.25
    #    b_inc = inc
    #    f_inc = inc * 0.5
    #    pri_i = inc * 2
    #    f_tshd = 10.0
    #    b_tshd = 50.0

    #    ssf = simple_stock_filter(volume_min, price_min, price_max, traced_weeks)
    #    ssf.run_filter(pri_i, f_inc, b_inc, f_tshd, b_tshd)

    #    print("parameter = %d" % i)
    #    print(ssf.stock_list)

