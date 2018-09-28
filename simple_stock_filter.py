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
#from pylab import mpl
#mpl.rcParams['font.sans-serif'] = ['msjh']



class simple_stock_filter:

    # dbg
    test_mode = 0
    stock_list = []

    def __init__(self, volume_min = 100000, price_min = 5.0, price_max = 200.0, traced_weeks = 2, waived_list = []):
        self.volume_min = volume_min
        self.price_min = price_min
        self.price_max = price_max
        self.traced_weeks = traced_weeks
        self.name_table = {}
        self.waived_list = waived_list

    def get_inst_inc(self, stock, days_traced):
        ss = inst_scrap(str(stock), days_traced)
        if(self.test_mode):
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if(len(ss.record_dates) > 0):
            print(ss.record_dates)
            sum = 0.0
            for d in ss.record_dates:
                inc = ss.data[d]['invest_diff_percent']
                sum += inc
            return sum*100
        else:
            logging.warn("No valid foreign data for %s" % stock)
            return 0.0

    def get_foreign_inc(self, stock, days_traced):
        ss = foreign_scrap(str(stock), days_traced)
        logging.info("handle %s" % str(stock))
        if(self.test_mode):
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if ss.set_data_failed:
            return 0.0
        if(len(ss.record_dates) > 0):
            print(ss.record_dates)
            if len(ss.record_dates)>5:
                rate = 5
            else:
                rate = 1
            sample_dates = self.sample_list(ss.record_dates, rate)
            start_date = sample_dates[-1]
            end_date = sample_dates[0]
            inc = ss.data[end_date] - ss.data[start_date]
            return inc
        else:
            logging.warn("No valid foreign data for %s" % stock)
            return 0.0

    def get_price_inc(self, stock, days_traced):
        ss = close_scrap(str(stock), days_traced)
        if self.test_mode:
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if(len(ss.record_dates) > 0):
            print(ss.record_dates)
            if len(ss.record_dates)>5:
                rate = 5
            else:
                rate = 1
            sample_dates = self.sample_list(ss.record_dates, rate)
            start_date = sample_dates[-1]
            end_date = sample_dates[0]
            try:
                inc = (ss.data[end_date]['close'] - ss.data[start_date]['close']) / ss.data[start_date]['close']
                return inc*100.0
            except TypeError:
                return 0.0
        else:
            logging.warn("No valid price data for %s" % stock)
            return 0.0

    def get_big_inc(self, stock, weeks_traced):
        ss = dist_scrap(str(stock), weeks_traced)
        if(self.test_mode):
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if(len(ss.record_dates) > 0):
            start_date = ss.record_dates[-1]
            end_date = ss.record_dates[0]
            threshold = 0.5
            inc = 0.0
            for level in [14, 13, 12, 11]:
                inc_segment = ss.data[end_date]['dist'][level]['percent'] - ss.data[start_date]['dist'][level]['percent']
                inc_segment_next = ss.data[end_date]['dist'][level-1]['percent'] - ss.data[start_date]['dist'][level-1]['percent']
                inc += inc_segment
                if abs(inc) > threshold:
                    break
                if inc_segment * inc_segment_next < 0:
                    # if next level goes to the opposite, we only use this elvel
                    break
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

    def waive(self):
        for w in self.waived_list:
            if w in self.stock_list:
                self.stock_list.remove(w)

    def run_viz_foreign_big(self):
        self.set_all_stock_list()
        today_str = str(datetime.date.today())
        if(self.test_mode):
            self.stock_list = ['2330', '2317', '2303']
        self.volume_over()
        self.waive()
        max_b = float("-inf")
        max_f = float("-inf")
        min_b = float("inf")
        min_f = float("inf")
        #plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        fig.set_size_inches(20, 15, forward = True)
        plt.title("近%d週外資大戶持股與股價變化(製表日:%s)" % (self.traced_weeks, today_str))
        plt.xlabel("外資持股變化(%)")
        plt.ylabel("大戶持股變化(%)")
        cnt = 1
        for stock in self.stock_list:
            days_traced = self.traced_weeks * 5 + 1
            weeks_traced = self.traced_weeks + 1
            p_inc = self.get_price_inc(stock, days_traced)
            f_inc = self.get_foreign_inc(stock, days_traced)
            b_inc = self.get_big_inc(stock, weeks_traced)
            max_f, min_f, max_b, min_b = self.update_bound(f_inc, b_inc, max_f, min_f, max_b, min_b)
            r, g, b = self.get_plot_color(p_inc)
            plot_text = self.get_plot_text(stock, p_inc)
            plt.text(f_inc, b_inc, plot_text, fontsize=4, color=(r, g, b))
            print(plot_text)
            print("%s: %f, %f, %f (%d of %d)" % (stock, f_inc, b_inc, p_inc, cnt, len(self.stock_list)))
            cnt += 1

        plt.axis([max_f, min_f, max_b, min_b])
        plt.savefig("./weekly_plot/%s 近%d週外資大戶持股變化.pdf" % (today_str, self.traced_weeks), dpi=300)
        plt.savefig("/mnt/c/Users/cm995/Desktop/plot_data/weekly_plot/%s 近%d週外資大戶持股變化.pdf" % (today_str, self.traced_weeks), dpi=300)

    def run_viz_inst_big(self):
        self.set_all_stock_list()
        today_str = str(datetime.date.today())
        if(self.test_mode):
            self.stock_list = ['2330', '2317', '2303']
        self.volume_over()
        self.waive()
        max_b = float("-inf")
        max_f = float("-inf")
        min_b = float("inf")
        min_f = float("inf")
        #plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus']=False
        fig, ax = plt.subplots()
        fig.set_size_inches(20, 15, forward = True)
        plt.title("近%d週投信大戶持股與股價變化(製表日:%s)" % (self.traced_weeks, today_str))
        plt.xlabel("投信持股變化(%)")
        plt.ylabel("大戶持股變化(%)")
        cnt = 1
        for stock in self.stock_list:
            days_traced = self.traced_weeks * 5 + 1
            weeks_traced = self.traced_weeks + 1
            p_inc = self.get_price_inc(stock, days_traced)
            f_inc = self.get_inst_inc(stock, days_traced)
            b_inc = self.get_big_inc(stock, weeks_traced)
            max_f, min_f, max_b, min_b = self.update_bound(f_inc, b_inc, max_f, min_f, max_b, min_b)
            r, g, b = self.get_plot_color(p_inc)
            plot_text = self.get_plot_text(stock, p_inc)
            plt.text(f_inc, b_inc, plot_text, fontsize=4, color=(r, g, b))
            print(plot_text)
            print("%s: %f, %f, %f (%d of %d)" % (stock, f_inc, b_inc, p_inc, cnt, len(self.stock_list)))
            cnt += 1

        plt.axis([max_f, min_f, max_b, min_b])
        plt.savefig("./weekly_plot/%s 近%d週投信大戶持股變化.pdf" % (today_str, self.traced_weeks), dpi=300)
        plt.savefig("/mnt/c/Users/cm995/Desktop/plot_data/weekly_plot/%s 近%d週投信大戶持股變化.pdf" % (today_str, self.traced_weeks), dpi=300)

    def run_daily_viz_foreign_inst(self):
        self.set_all_stock_list()
        today_str = str(datetime.date.today())
        if(self.test_mode):
            self.stock_list = ['2330', '2317', '2303']
        self.volume_over()
        self.waive()
        max_b = float("-inf")
        max_f = float("-inf")
        min_b = float("inf")
        min_f = float("inf")
        #plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()
        fig.set_size_inches(20, 15, forward = True)
        plt.title("外資投信持股與股價變化(製表日:%s)" % today_str)
        plt.xlabel("外資持股變化(%)")
        plt.ylabel("投信持股變化(%)")
        cnt = 1
        for stock in self.stock_list:
            days_traced = 1
            p_inc = self.get_price_inc(stock, days_traced+1)
            f_inc = self.get_foreign_inc(stock, days_traced+1)
            i_inc = self.get_inst_inc(stock, days_traced)
            max_f, min_f, max_b, min_b = self.update_bound(f_inc, i_inc, max_f, min_f, max_b, min_b)
            r, g, b = self.get_plot_color(p_inc)
            plot_text = self.get_plot_text(stock, p_inc)
            plt.text(f_inc, i_inc, plot_text, fontsize=4, color=(r, g, b))
            print(plot_text)
            print("%s: %f, %f, %f (%d of %d)" % (stock, f_inc, i_inc, p_inc, cnt, len(self.stock_list)))
            cnt += 1

        plt.axis([max_f, min_f, max_b, min_b])
        plt.savefig("./daily_plot/%s外資投信持股變化.pdf" % today_str, dpi=300)
        plt.savefig("/mnt/c/Users/cm995/Desktop/plot_data/daily_plot/%s外資投信持股變化.pdf" % today_str, dpi=300)

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
        url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date='
        date_str = ss.get_date_string(ss.today)
        data_part = None
        while data_part is None:
            try:
                html_str = ss.get_html_str(url)
                raw_data = eval(html_str)
                data_part = raw_data['data']
            except KeyError:
                logging.info("retry...")
                ss.today -= datetime.timedelta(1)
                date_str = ss.get_date_string(ss.today)
                pass
        all_stock_list = []
        for stock in data_part:
            stock_id = stock[0]
            stock_name = stock[1]
            pat = re.compile('^[1-9]\d{3}$')
            if(pat.match(stock_id)):
                all_stock_list.append(stock_id)
                self.name_table[stock_id] = stock_name.strip()
        logging.debug("all_stock_list: %s" % str(all_stock_list))
        self.stock_list = all_stock_list


if __name__ == "__main__":
    logging.basicConfig(filename='ssf.log', level=logging.DEBUG)
    volume_min = 100000
    price_min = 5.0
    price_max = 5000.0
    waived_list = ['2614', '2208']
    for i in range(4):
        traced_weeks = i + 1
        ssf = simple_stock_filter(volume_min, price_min, price_max, traced_weeks, waived_list)
        ssf.run_viz_foreign_big()
        ssf.run_viz_inst_big()

