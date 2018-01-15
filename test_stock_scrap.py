#!/usr/bin/python3
from stock_scrap import stock_scrap
import unittest
import datetime

class test_stock_scrap(unittest.TestCase):

    def test_pure(self):
        ss = stock_scrap("3035", 21, "")
        self.assertEqual(ss.get_pure_int(" 321, 21.000"), 32121)
        self.assertEqual(ss.get_pure_float(" 321, 21.0001"), float(32121.0001))
        self.assertEqual(ss.get_pure_float("32.1"), float(32.1))

if __name__ == '__main__':
    unittest.main()
