#!/usr/bin/python3
from simple_stock_filter import simple_stock_filter
import unittest
import logging

class test_simple(unittest.TestCase):

    test_set = ['2890', '2836', '1806', '2889', '2537', '2705', '6152', '3052', '1618', '1423', '1810', '2845', '2305', '6142', '3047', '2363']

    def test_price_now(self):
        ss = simple_stock_filter()
        ss.test_mode = 1
        ss.set_all_stock_list()
        ss.stock_list = self.test_set
        ss.price_now(10, 8, 3, 0.0)
        self.assertEqual(ss.stock_list, ['1618', '3047', '2363'])

    def test_foreign_percent(self):
        ss = simple_stock_filter()
        #ss.test_mode = 1
        ss.stock_list = self.test_set
        ss.foreign_percent(0.0, 3, .0)
        print(ss.stock_list)


    def test_dist_percent(self):
        ss = simple_stock_filter()
        #ss.test_mode = 1
        ss.stock_list = self.test_set
        lvl = 14
        ss.big_owner_percent(lvl , 0.0, 3, .0)
        print(ss.stock_list)


    def test_dict_to_list(self):
        ss = simple_stock_filter()
        trial = {"20170102":"first", "20180101":"third", "20171212":"second"}
        sorted_list = ss.dict_to_list(trial, 0)
        reversed_list = ss.dict_to_list(trial, 1)
        self.assertEqual(sorted_list[0], "first")
        self.assertEqual(reversed_list[0], "third")


if __name__ == '__main__':
    logging.basicConfig(filename='test_simple.log', level=logging.DEBUG)
    unittest.main()
