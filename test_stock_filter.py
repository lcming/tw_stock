#!/usr/bin/python3

from dist_scrap import dist_scrap
from stock_scrap import stock_scrap
from inst_scrap import inst_scrap
from price_scrap import price_scrap
import unittest
import logging

class test_dist_scrap(unittest.TestCase):

    def build_sample_stock_filter(self):
        sf = stock_filter()
        sf.stock_id_set = [3034, 3035]
        sf.test_mode = 1
        sf.set_all()
        return sf

    def filt_by_price_now(self):
        sf = self.build_sample_stock_filter()
        sf.filt_by_price_now()
        self.assertIn(3035, sf.stock_id_set)
        self.assertNotIn(3034, sf.stock_id_set)

    def set_dist(self):
        return

    def set_price(self):
        return

    def set_inst(self):
        return

    def get_all_stock_list(self):
        sf = stock_filter()
        stock_list = sf.get_all_stock_list()
        self.assertIn(1102, stock_list)
        self.assertIn(1210, stock_list)
        self.assertIn(1714, stock_list)
        self.assertIn(1605, stock_list)
        self.assertIn(2353, stock_list)
        self.assertIn(9945, stock_list)
        self.assertIn(9962, stock_list)

if __name__ == '__main__':
    logging.basicConfig(filename='test_dist_scrap.log', level=logging.DEBUG)
    unittest.main()
