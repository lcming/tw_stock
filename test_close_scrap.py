#!/usr/bin/python3
from close_scrap import close_scrap
from test_scrap_template import test_scrap_template
import unittest
import logging


class test_close_scrap(test_scrap_template):

    def setUp(self):
        super().setUp()
        self.check_points = {'20180418': {'close': 65.2, 'open': 67.1, 'high': 67.3, 'deal_shares': 4509226, 'deal_count': 2816.0, 'low': 64.2, 'deal_value': 295550000.0}, '20180417': {'close': 66.4, 'open': 67.0, 'high': 67.4, 'deal_shares': 2643837, 'deal_count': 1839.0, 'low': 66.1, 'deal_value': 176262661.0}, '20180414': None, '20180413': {'close': 65.0, 'open': 66.2, 'high': 66.6, 'deal_shares': 3265546, 'deal_count': 2108.0, 'low': 64.8, 'deal_value': 213377590.0}, '20180419': {'close': 68.8, 'open': 66.1, 'high': 68.8, 'deal_shares': 5055825, 'deal_count': 3513.0, 'low': 65.5, 'deal_value': 341450747.0}, '20180420': {'close': 67.1, 'open': 68.0, 'high': 68.6, 'deal_shares': 3292807, 'deal_count': 2280.0, 'low': 67.0, 'deal_value': 222814838.0}, '20180415': None, '20180416': {'close': 66.8, 'open': 65.5, 'high': 67.8, 'deal_shares': 3478409, 'deal_count': 2480.0, 'low': 65.1, 'deal_value': 231714590.0}}

    def setUp(self):
        super().setUp()

    def build_scrap(self):
        ss = close_scrap("3035", 6)
        return ss

    def test_data(self):
        super().check_data()

    def test_data_scratch(self):
        super().check_data_scratch()

if __name__ == '__main__':
    logging.basicConfig(filename='test_close_scrap.log', level=logging.DEBUG)
    unittest.main()
