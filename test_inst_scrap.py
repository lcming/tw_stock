#!/usr/bin/python3
from inst_scrap import inst_scrap
from stock_scrap import stock_scrap
import unittest
import logging
import os, glob


class test_inst_scrap(unittest.TestCase):
    fix_year = 2018
    fix_month = 4
    fix_day = 20

    def test_format_url(self):
        inss = inst_scrap("2303", 3)
        ex_url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201'
        self.assertEqual(inss.format_url("20171201"), ex_url)
        self.assertNotEqual(inss.format_url("20161001"), ex_url)


    def test_data(self):
        inss = inst_scrap("3035", 6)
        inss.set_today(self.fix_year, self.fix_month, self.fix_day)
        inss.set_data()
        self.assertEqual(inss.data["20180420"]['dealer_buy_hedge'], 55000)
        self.assertEqual(inss.data["20180419"]['total_diff'], 1741000)
        self.assertEqual(inss.data["20180418"]['invest_buy'], 0)
        self.assertAlmostEqual(inss.data["20180417"]['invest_diff_percent'], 0.0002011665139202621 )
        self.assertEqual(inss.data["20180416"]['foreign_diff'], 536000)
        self.assertIsNone(inss.data["20180415"])

    def test_data_scratch(self):
        files = glob.glob('./cache_scratch/*')
        for f in files:
            os.remove(f)
        stock_scrap.scratch_mode = 1
        self.test_data()

if __name__ == '__main__':
    logging.basicConfig(filename='test_inst_scrap.log', level=logging.DEBUG)
    unittest.main()
