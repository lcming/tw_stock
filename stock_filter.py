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
    max_price = 100
    min_price = 20
    big_holder_portion = 70.0
    big_holder_criteria_by_share = 200000
    big_holder_criteria_by_value = 200000000.1
    big_holder_criteria = 1 # 1: by share, 0: by value
    foreign_diff_increased = 15.0

    def dbg(self):
        print("--- price array ---")
        print(self.price)
        print("--- total shares array ---")
        print(self.total_shares)
        print("--- owners dist array ---")
        print(self.owners_dist)
        print("--- percent dist array ---")
        print(self.percent_dist)

    def set_parameters(self):
        return
    def set_price(self):
        price_2d_array = []
        for stock_id in self.stock_id_set:
            ps = price_scrap(stock_id, self.days_traced)
            ps.set_data()
            trace_in_range = self.get_sorted_data_in_range(ps.data, self.days_traced)
            price_2d_array.append(trace_in_range)
        self.price = np.array(price_2d_array)
        return

    def set_total_shares(self):
        return
    def set_foreign_diff(self):
        return
    def get_sorted_data_in_range(self, data, _range):
        sorted_data = collections.OrderedDict(sorted(data.items()))
        value_only_od = sorted_data.values()
        value_only_list = list(value_only_od)
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
        for stock_id in self.stock_id_set:
            ds = dist_scrap(stock_id, self.days_traced)
            ds.set_data()
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
