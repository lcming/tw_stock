from price_scrap import price_scrap
from dist_scrap import dist_scrap
from inst_scrap import inst_scrap
import datetime
import collections
import numpy as np

class stock_filter:

    # basic info.
    days_traced = None
    stock_id_set = None

    # numpy matrix
    price = None# 2d-mat, x: day, y: stock
    foreign_diff = None#2d-mat, x: day, y: stock
    total_shares = None# 1d
    owners_dist = None# 3d-mat, x: day, y: stock, z: dist
    percent_dist = None# 3d-mat, x: day, y: stock, z: dist

    # parameters
    max_price = 100.
    min_price = 10.
    big_holder_portion = 70.0
    foreign_diff_increased = 15.0

    # dbg
    y = 2017
    m = 12
    d = 29
    test_mode = 0


    def remove_stocks(self, rm_list):
        for rm_idx in reversed(rm_list):
            self.stock_id_set.remove(self.stock_id_set[rm_idx])
        self.price = np.delete(self.price, rm_list, 0)
        self.foreign_diff = np.delete(self.foreign_diff, rm_list)
        self.total_shares = np.delete(self.total_shares, rm_list)
        self.owners_dist = np.delete(self.owners_dist, rm_list)
        self.percent_dist = np.delete(self.percent_dist, rm_list)


    def filt_by_price_now(self):
        rm_list = []
        print(self.price)
        for i in range(0, len(self.stock_id_set)):
            if( self.price[i][0] < self.min_price or self.price[i][0] > self.max_price):
                rm_list.append(i)
        self.remove_stocks(rm_list)

    def dbg(self):
        print("--- price array ---")
        print(self.price)
        print("--- total shares array ---")
        print(self.total_shares)
        print("--- owners dist array ---")
        print(self.owners_dist)
        print("--- percent dist array ---")
        print(self.percent_dist)
        print("--- foreign diff array ---")
        print(self.foreign_diff)

    def get_acc_matrix(self, width):
        acc_2d_arrary = []
        last_zero_idx = 0
        for i in range(0, width):
            acc_array = []
            for j in range(0, width):
                if (j < last_zero_idx):
                    acc_array.append(0.0)
                else:
                    acc_array.append(1.0)
            last_zero_idx += 1
            acc_2d_arrary.append(acc_array)
        return np.array(acc_2d_arrary)


    def get_ma_matrix(self, ma_width, total_width):
        ma_2d_array = []
        weight = 1.0 / ma_width
        for i in range(0, total_width):
            row = []
            for j in range(0, total_width):
                if(i >= j and i < j + ma_width):
                    out_bound = j + ma_width - total_width
                    if(out_bound > 0):
                        bound_weight = 1.0 / (ma_width - out_bound)
                        row.append(bound_weight)
                    else:
                        row.append(weight)
                else:
                    row.append(0)
            ma_2d_array.append(row)
        return np.array(ma_2d_array)

    def set_parameters(self):
        return
    def set_price(self):
        price_2d_array = []
        for stock_id in self.stock_id_set:
            ps = price_scrap(stock_id, self.days_traced)
            if(self.test_mode):
                ps.set_today(self.y, self.m, self.d )
            ps.set_data()
            trace_in_range = self.get_sorted_data_in_range(ps.data, self.days_traced)
            price_2d_array.append(trace_in_range)
        self.price = np.array(price_2d_array)
        return

    def get_scalar_array_from_hash_array(self, hash_array, key):
        scalar_array = []
        for item in hash_array:
            scalar_array.append(item[key])
        return scalar_array

    def set_foreign_diff(self):
        diff_2d_array = []
        for stock_id in self.stock_id_set:
            ins = inst_scrap(stock_id, self.days_traced)
            if(self.test_mode):
                ins.set_today(self.y, self.m, self.d )
            ins.set_data()
            trace_in_range = self.get_sorted_data_in_range(ins.data, self.days_traced)
            diff_array = self.get_scalar_array_from_hash_array(trace_in_range, 'foreign_diff')
            diff_2d_array.append(diff_array)
        self.foreign_diff = np.array(diff_2d_array)
        return
    def get_sorted_data_in_range(self, data, _range):
        sorted_data = []
        for i in sorted(data):
            sorted_data.append(data[i])
        value_only_list = list(reversed(sorted_data))
        return value_only_list[0:_range]

    def get_pure_array_by_keyword(self, data, keyword):
        dist = []
        for daily_data in data:
            daily_dist = []
            for level in daily_data['dist']:
                daily_dist.append(level[keyword])
            dist.append(daily_dist)
        return dist

    def set_dist(self):
        total_shares_1d_array = []
        owners_dist_3d_array = []
        percent_dist_3d_array = []
        weeks_traced = self.days_traced / 7 + 1
        for stock_id in self.stock_id_set:
            ds = dist_scrap(stock_id, weeks_traced)
            if(self.test_mode):
                ds.set_today(self.y, self.m, self.d )
            ds.set_data()
            ds.dbg()
            trace_in_range = self.get_sorted_data_in_range(ds.data, self.days_traced)
            trace_in_range
            last_day_total_shares = trace_in_range[-1]['total_shares']
            total_shares_1d_array.append(last_day_total_shares)
            owners_dist_per_stock = self.get_pure_array_by_keyword(trace_in_range, 'owners')
            percent_dist_per_stock = self.get_pure_array_by_keyword(trace_in_range, 'percent')
            owners_dist_3d_array.append(owners_dist_per_stock)
            percent_dist_3d_array.append(percent_dist_per_stock)
        self.total_shares = np.array(total_shares_1d_array)
        self.percent_dist = np.array(percent_dist_3d_array)
        self.owners_dist = np.array(owners_dist_3d_array)
        return
