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
    total_shares = None# 1d
    foreign_diff = None#2d-mat, x: day, y: stock
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

    def set_parameters(self):
        return
    def set_price(self):
        price_2d_array = []
        for stock_id in self.stock_id_set:
            ps = price_scrap(stock_id, self.days_traced)
            ps.set_data()
            price_2d_array.append(list(collections.OrderedDict(sorted(ps.data.items())).values())[0:self.days_traced])
        self.price = np.array(price_2d_array)
        print(self.price)
        return



    def set_total_shares(self):
        return
    def set_foreign_diff(self):
        return
    def set_owners_dist(self):
        return
    def set_percent_dist(self):
        return
