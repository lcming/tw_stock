# -*- coding: utf-8 -*-
from price_scrap import price_scrap
from dist_scrap import dist_scrap
from inst_scrap import inst_scrap
from foreign_scrap import foreign_scrap
from close_scrap import close_scrap
from stock_scrap import *
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

    def __init__(self, volume_min = 500000, price_min = 5.0, price_max = 200.0, traced_weeks = 2, waived_list = []):
        self.volume_min = volume_min
        self.price_min = price_min
        self.price_max = price_max
        self.traced_weeks = traced_weeks
        self.name_table = {}
        self.waived_list = waived_list
        self.bull = []
        self.bear = []
        self.lai_bear = []

    def get_inst_inc(self, stock, days_traced):
        ss = inst_scrap(str(stock), days_traced)
        if(self.test_mode):
            ss.set_today(2018, 1, 5)
        ss.set_data()
        if(len(ss.record_dates) > 0):
            #print(ss.record_dates)
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
            #print(ss.record_dates)
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
            #print(ss.record_dates)
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
        self.waive()

    def get_avg_data(self, stock_id, days_traced, tag):
        ss = close_scrap(str(stock_id), days_traced)
        if(self.test_mode):
            ss.set_today(2018, 9, 28)
        ss.set_data()
        acc = 0.0
        day = 0
        no_trade_day = 0
        for i in reversed(sorted(ss.data)):
            if ss.data[i]:
                try:
                    acc += ss.data[i][tag]
                except TypeError:
                    no_trade_day += 1
                day += 1
            if day == days_traced:
                break
        if day == no_trade_day:
            raise StockTraceException("No trade")
        return acc / (day-no_trade_day)

    def scan_price_volume_breakout_bull(self, vol_inc_over_5_20_ma, price_ma_tangle_window):
        for stock in self.stock_list:
            try:
                chip_ok = 0
                price_breakout_ok = 0
                vol_breakout_ok = 0
                vol_ok = 0
                recent_price = self.get_avg_data(stock, 1, 'close')
                recent_open = self.get_avg_data(stock, 1, 'open')
                recent_high = self.get_avg_data(stock, 1, 'high')
                recent_low = self.get_avg_data(stock, 1, 'low')
                recent_vol = self.get_avg_data(stock, 1, 'deal_shares')
                prev_price = self.get_avg_data(stock, 2, 'close') * 2 - recent_price
                price_5ma = self.get_avg_data(stock, 5, 'close')
                price_20ma = self.get_avg_data(stock, 20, 'close')
                vol_5ma = self.get_avg_data(stock, 5, 'deal_shares')
                vol_20ma = self.get_avg_data(stock, 20, 'deal_shares')
                foreign_weekly_inc = self.get_foreign_inc(stock, 5+1)
                inst_weekly_inc = self.get_inst_inc(stock, 5+1)
                sign_ok = self.check_close_sign_bull(prev_price, recent_price, recent_open, recent_high, recent_low)
                if foreign_weekly_inc + inst_weekly_inc > 0.0:
                    chip_ok = 1
                if abs(self.diff_percent(recent_price, price_5ma)) < price_ma_tangle_window and abs(self.diff_percent(price_5ma, price_20ma)) < price_ma_tangle_window:
                    price_breakout_ok = 1
                if self.diff_percent(recent_vol, vol_5ma) > vol_inc_over_5_20_ma and self.diff_percent(recent_vol, vol_20ma) > vol_inc_over_5_20_ma:
                    vol_breakout_ok = 1
                if vol_20ma > 300.0:
                    vol_ok = 1
                if chip_ok and price_breakout_ok and vol_breakout_ok and vol_ok and sign_ok:
                    print("%s passed!" % stock)
                    self.bull.append(stock)
            except StockTraceException:
                print("%s ignored!" % stock)
                next;

    def scan_price_volume_breakout_bear(self, vol_inc_over_5_20_ma, price_ma_tangle_window):
        for stock in self.stock_list:
            try:
                chip_ok = 0
                price_breakout_ok = 0
                vol_breakout_ok = 0
                recent_price = self.get_avg_data(stock, 1, 'close')
                recent_open = self.get_avg_data(stock, 1, 'open')
                recent_high = self.get_avg_data(stock, 1, 'high')
                recent_low = self.get_avg_data(stock, 1, 'low')
                recent_vol = self.get_avg_data(stock, 1, 'deal_shares')
                prev_price = self.get_avg_data(stock, 2, 'close') * 2 - recent_price
                price_5ma = self.get_avg_data(stock, 5, 'close')
                price_20ma = self.get_avg_data(stock, 20, 'close')
                vol_5ma = self.get_avg_data(stock, 5, 'deal_shares')
                vol_20ma = self.get_avg_data(stock, 20, 'deal_shares')
                foreign_weekly_inc = self.get_foreign_inc(stock, 5+1)
                inst_weekly_inc = self.get_inst_inc(stock, 5+1)
                sign_ok = self.check_close_sign_bear(prev_price, recent_price, recent_open, recent_high, recent_low)
                if foreign_weekly_inc + inst_weekly_inc < 0.0:
                    chip_ok = 1
                if abs(self.diff_percent(recent_price, price_5ma)) < price_ma_tangle_window and abs(self.diff_percent(price_5ma, price_20ma)) < price_ma_tangle_window:
                    price_breakout_ok = 1
                if self.diff_percent(recent_vol, vol_5ma) > vol_inc_over_5_20_ma and self.diff_percent(recent_vol, vol_20ma) > vol_inc_over_5_20_ma:
                    vol_breakout_ok = 1
                if vol_20ma > 300.0:
                    vol_ok = 1
                if chip_ok and price_breakout_ok and vol_breakout_ok and vol_ok and sign_ok:
                    print("%s passed!" % stock)
                    self.bear.append(stock)
            except StockTraceException:
                print("%s ignored!" % stock)
                next;

    def scan_lai_bear(self, vol_inc, plunge, ma_5_20_diff, ma_20_60_diff):
        for stock in self.stock_list:
            try:
                chip_ok = 0
                price_breakout_ok = 0
                vol_breakout_ok = 0
                price_break_60ma = 0
                recent_price = self.get_avg_data(stock, 1, 'close')
                recent_open = self.get_avg_data(stock, 1, 'open')
                recent_high = self.get_avg_data(stock, 1, 'high')
                recent_low = self.get_avg_data(stock, 1, 'low')
                prev_price = self.get_avg_data(stock, 2, 'close') * 2 - recent_price
                recent_vol = self.get_avg_data(stock, 1, 'deal_shares')
                price_5ma = self.get_avg_data(stock, 5, 'close')
                price_20ma = self.get_avg_data(stock, 20, 'close')
                price_60ma = self.get_avg_data(stock, 60, 'close')
                vol_20ma = self.get_avg_data(stock, 20, 'deal_shares')
                vol_yesterday = (self.get_avg_data(stock, 2, 'deal_shares') - 0.5 * recent_vol) * 2.0
                price_yesterday = (self.get_avg_data(stock, 2, 'close') - 0.5 * recent_price) * 2.0
                foreign_weekly_inc = self.get_foreign_inc(stock, 5+1)
                inst_weekly_inc = self.get_inst_inc(stock, 5+1)
                if foreign_weekly_inc + inst_weekly_inc < 0.0:
                    chip_ok = 1
                if self.diff_percent(recent_price, price_yesterday) < -plunge and abs(self.diff_percent(price_5ma, price_20ma)) < ma_5_20_diff and abs(self.diff_percent(price_20ma, price_60ma)) < ma_20_60_diff:
                    price_breakout_ok = 1
                if self.diff_percent(recent_vol, vol_yesterday) > vol_inc and self.diff_percent(recent_vol, vol_20ma) > vol_inc:
                    vol_breakout_ok = 1
                if chip_ok and price_breakout_ok and vol_breakout_ok and simple_stock_filter and self.check_close_sign_bear(prev_price, recent_price, recent_open, recent_high, recent_low):
                    print("%s passed!" % stock)
                    self.lai_bear.append(stock)
            except StockTraceException:
                print("%s ignored!" % stock)
                continue

    def check_close_sign_bear(self, p, c, o, h, l):
        gain = c - p
        k_body = c - o
        up_stick = abs(o - h)
        down_stick = abs(c - l)
        if gain < 0 and k_body < 0 and (abs(k_body) + up_stick > down_stick):
            return 1
        else:
            return 0

    def check_close_sign_bull(self, p, c, o, h, l):
        gain = c > p
        k_body = c - o
        up_stick = h - c
        down_stick = o - l
        if k_body > 0 and gain and (k_body + down_stick > up_stick):
            return 1
        else:
            return 0

    def diff_percent(self, a, b):
        return float(a-b)/b*100


if __name__ == "__main__":
    log_name = 'ssf.log'
    logging.basicConfig(filename='ssf.log', level=logging.DEBUG)
    stock_scrap.trace_bound = "20180701"
    waived_list = ['2108']
    ssf = simple_stock_filter(volume_min = 500000, waived_list=waived_list)
    ssf.set_all_stock_list()
    ssf.volume_over()
    ssf.scan_price_volume_breakout_bull(50.0, 5)
    ssf.scan_price_volume_breakout_bear(50.0, 5)
    ssf.scan_lai_bear(50.0, 3, 10, 20)
    print("bull:")
    print(ssf.bull)
    print("bear:")
    print(ssf.bear)
    print("lai bear:")
    print(ssf.lai_bear)
    #volume_min = 100000
    #price_min = 5.0
    #price_max = 5000.0
    #for i in range(4):
    #    traced_weeks = i + 1
    #    ssf = simple_stock_filter(volume_min, price_min, price_max, traced_weeks, waived_list)
    #    ssf.run_viz_foreign_big()
    #    ssf.run_viz_inst_big()
