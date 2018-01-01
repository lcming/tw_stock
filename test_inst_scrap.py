#!/usr/bin/python3
from inst_scrap import inst_scrap
import unittest
import datetime
import logging
import sys
import os


class test_inst_scrap(unittest.TestCase):
    fix_year = 2017
    fix_month = 12
    fix_day = 1

    def test_format_url(self):
        inss = inst_scrap("2303", 3)
        ex_url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201'
        self.assertEqual(inss.format_url("20171201"), ex_url)
        self.assertNotEqual(inss.format_url("20161001"), ex_url)


    def test_set_data(self):
        inss = inst_scrap("3035", 22)
        inss.set_today(2017, 11, 30)
        inss.set_data()
        self.assertEqual(inss.data["20171031"]['foreign_buy'], 671000)
        self.assertEqual(inss.data["20171101"]['dealer_buy_hedge'], 125000)
        self.assertEqual(inss.data["20171129"]['total_diff'], 5041000)
        self.assertEqual(inss.data["20171130"]['invest_buy'], 173000)

    def test_cache_data(self):
        tmp_cache_name = "tmp_cache_for_test.txt"
        if(os.path.isfile(tmp_cache_name)):
            os.remove(tmp_cache_name)

        inss = inst_scrap("3035", 10)
        inss.set_today(2017, 11, 30)
        if('flush' in os.environ):
            inss.cache_name = tmp_cache_name
        inss.set_data()

        inss = inst_scrap("3035", 10)
        inss.set_today(2017, 12, 1)
        if('flush' in os.environ):
            inss.cache_name = tmp_cache_name
        inss.set_data()

        if('flush' in os.environ):
            # 9 hits on valid trade, 2 hits on no trade
            self.assertEqual(inss.hit_count, 11)
        self.assertEqual(inss.data['20171201']['foreign_diff'], -731200)
        self.assertEqual(inss.data['20171130']['foreign_diff'], 2443000)
        self.assertEqual(inss.data['20171117']['foreign_diff'], -1448000)
        self.assertEqual(inss.data['20171118'], None)

    #def test_get_stock_id_idx(self):
    #    inss = inst_scrap("2330", 3)
    #    ex_url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201'
    #    raw_data = eval(inss.get_html_str(ex_url))
    #    data_part = raw_data['data']
    #    self.assertEqual(inss.get_stock_id_idx(data_part, "00632R"), 0)
    #    self.assertEqual(inss.get_stock_id_idx(data_part, "2882"), 1)
    #    self.assertEqual(inss.get_stock_id_idx(data_part, "2891"), 2)
    #    self.assertEqual(inss.get_stock_id_idx(data_part, "00637L"), 8886)


if __name__ == '__main__':
    logging.basicConfig(filename='test_inst_scrap.log', level=logging.DEBUG)
    unittest.main()
