#!/usr/bin/python3
from price_scrap import price_scrap
from test_scrap_template import test_scrap_template
import logging
import unittest

class test_price_scrap(test_scrap_template):

    def setUp(self):
        super().setUp()
        self.check_points = {'20180426': 15.7, '20180324': None, '20180412': 15.45, '20180312': 15.25, '20180322': 15.25, '20180306': 14.15, '20180419': 15.85, '20180313': 15.25, '20180309': 15.1, '20180330': 15.4, '20180320': 15.2, '20180424': 15.35, '20180308': 15.45, '20180404': None, '20180327': 15.55, '20180311': None, '20180328': 15.4, '20180323': 15.2, '20180405': None, '20180307': 14.05, '20180423': 15.55, '20180301': 14.0, '20180310': None, '20180407': None, '20180406': None, '20180413': 15.4, '20180318': None, '20180418': 15.6, '20180325': None, '20180317': None, '20180417': 15.35, '20180331': 15.5, '20180316': 15.2, '20180430': 16.0, '20180305': 13.9, '20180319': 15.25, '20180410': 15.3, '20180408': None, '20180329': 15.3, '20180420': 15.6, '20180314': 15.1, '20180414': None, '20180403': 15.4, '20180409': 15.25, '20180401': None, '20180427': 15.7, '20180321': 15.2, '20180425': 15.5, '20180415': None, '20180416': 15.35, '20180326': 15.15, '20180315': 15.1, '20180302': 14.0, '20180402': 15.45, '20180411': 15.4}

    def build_scrap(self):
        ss = price_scrap("2303", 31)
        return ss

    def test_format_date(self):
        ps = price_scrap("2303", 31)
        ps.set_today(2017, 11, 30)
        self.assertEqual(ps.format_date("82/05/18"), "19930518")

    def test_format_url(self):
        ps = price_scrap("2303", 3)
        ex_url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303'
        self.assertEqual(ps.format_url("20171001"), ex_url)
        self.assertNotEqual(ps.format_url("20161001"), ex_url)

    def test_data(self):
        super().check_data()

    def test_data_scratch(self):
        super().check_data_scratch()

if __name__ == '__main__':
    logging.basicConfig(filename='test_price_scrap.log', level=logging.DEBUG)
    unittest.main()
