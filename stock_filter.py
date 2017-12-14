from price_scrap import price_scrap
from dist_scrap import dist_scrap
from inst_scrap import inst_scrap

class stock_filter:

    # basic info.
    days_traced
    stock_id_set = []

    # numpy matrix
    price # 2d-mat, x: day, y: stock
    total_shares # 1d
    foreign_diff #2d-mat, x: day, y: stock
    owners_dist # 3d-mat, x: day, y: stock, z: dist
    percent_dist # 3d-mat, x: day, y: stock, z: dist

    # scraps
    ps
    ds
    ins

    # parameters
    max_price
    min_price
    big_holder_portion
    big_holder_criteria_by_share
    big_holder_criteria_by_value
    big_holder_criteria # 1: by share, 0: by value
    foreign_diff_increased

    def set_parameters(self):
    def set_scraps(self):
    def set_price(self):
    def set_total_shares(self):
    def set_foreign_diff(self):
    def set_owners_dist(self):
    def set_percent_dist(self):
