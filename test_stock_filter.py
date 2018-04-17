#!/usr/bin/python3

from stock_filter import stock_filter
import unittest
import logging
import numpy as np

class test_stock_filter(unittest.TestCase):

    def build_sample_stock_filter(self):
        sf = stock_filter()
        sf.stock_id_set = [3034, 3035]
        sf.test_mode = 1
        sf.days_traced = 10
        sf.set_all()
        return sf

    #def test_filt_by_price_now(self):
    #    sf = self.build_sample_stock_filter()
    #    sf.filt_by_price_now()
    #    self.assertIn(3035, sf.stock_id_set)
    #    self.assertNotIn(3034, sf.stock_id_set)

    #def test_set_all(self):
    #    sf = self.build_sample_stock_filter()
    #    for i in (sf.price, sf.foreign_diff,sf.total_shares, sf.owners_dist, sf.percent_dist):
    #        self.assertEqual(np.size(i, 0), 2)
    #    for i in (sf.price, sf.foreign_diff):
    #        self.assertEqual(np.size(i, 1), 10)

    #    sf.dbg()

    #    return

    #def test_get_all_stock_list(self):
    #    sf = stock_filter()
    #    stock_list = sf.get_all_stock_list()
    #    self.assertIn(1102, stock_list)
    #    self.assertIn(1210, stock_list)
    #    self.assertIn(1714, stock_list)
    #    self.assertIn(1605, stock_list)
    #    self.assertIn(2353, stock_list)
    #    self.assertIn(9945, stock_list)

    #def test_set_dist(self):
    #    sf = stock_filter()
    #    sf.stock_id_set = [3034, 3035]
    #    sf.test_mode = 1
    #    sf.days_traced = 10
    #    sf.set_dist()
    #    sf.dbg()
        for i in (sf.percent_dist, sf.owners_dist):
            self.assertEqual(np.size(i), 60)
            self.assertEqual(np.size(i, 0), 2)
            self.assertEqual(np.size(i, 1), 2)
            self.assertEqual(np.size(i, 2), 15)

if __name__ == '__main__':
    logging.basicConfig(filename='test_stock_filter.log', level=logging.DEBUG)
    #unittest.main()
