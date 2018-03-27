#!/usr/bin/python3
from simple_stock_filter import simple_stock_filter
import unittest
import logging

class test_simple(unittest.TestCase):

    test_set = ['2890', '2836', '1806', '2889', '2537', '2705', '6152', '3052', '1618', '1423', '1810', '2845', '2305', '6142', '3047', '2363']

    volume_min = 100000
    price_min = 5.0
    price_max = 200.0
    traced_weeks = 2

    def test_inc(self):
        ss = simple_stock_filter()
        ss.test_mode = 1
        stock = '2330'
        p_inc = ss.get_price_inc(stock)
        f_inc = ss.get_foreign_inc(stock)
        b_inc = ss.get_big_inc(stock)
        self.assertAlmostEqual(p_inc, 6.666666666666667)
        self.assertAlmostEqual(f_inc, 0.15)
        self.assertAlmostEqual(b_inc, 0.06)

    def test_set_all_stock_list(self):
        ss = simple_stock_filter()
        ss.set_all_stock_list()
        print("total stock = %d" % len(ss.stock_list))

    def test_price_window_inc_below(self):
        ss = simple_stock_filter(self.volume_min, 8.0, 10.0, 0)
        ss.test_mode = 1
        ss.stock_list = self.test_set
        ss.price_window_inc_below(float('inf'))
        self.assertEqual(self.test_set, ss.stock_list)


    def test_foreign_inc_over(self):
        ss = simple_stock_filter()
        ss.test_mode = 1
        ss.stock_list = self.test_set
        ss.foreign_inc_over(10.0, 0.0)
        self.assertEqual(ss.stock_list, ['2890', '1806', '2889'])

    def test_big_inc_over(self):
        ss = simple_stock_filter()
        ss.test_mode = 1
        ss.stock_list = self.test_set
        lvl = 14
        ss.big_inc_over(lvl , 50.0, 0.0)
        self.assertEqual(ss.stock_list, ['2890', '2836', '3052', '2845'])

if __name__ == '__main__':
    logging.basicConfig(filename='test_simple.log', level=logging.DEBUG)
    unittest.main()
