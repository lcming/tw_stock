#!/usr/bin/python3
from price_scrap import price_scrap
from stock_scrap import stock_scrap
import unittest
import datetime
import logging
import os

class test_dist_scrap(unittest.TestCase):
    fix_year = 2017
    fix_month = 11
    fix_day = 30
    def test_format_date(self):
        ps = price_scrap("2303", 31)
        ps.set_today(2017, 11, 30)
        self.assertEqual(ps.format_date("82/05/18"), "19930518")

    def test_format_url(self):
        ps = price_scrap("2303", 3)
        ex_url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303'
        self.assertEqual(ps.format_url("20171001"), ex_url)
        self.assertNotEqual(ps.format_url("20161001"), ex_url)


    def test_set_data(self):
        ps = price_scrap("3035", 22)
        ps.set_today(2017, 11, 30)
        ps.set_data()
        self.assertEqual(ps.data["20171127"], 58.4)
        self.assertEqual(ps.data["20171128"], 57.3)
        self.assertEqual(ps.data["20171129"], 63)
        self.assertIn("20171101", ps.data)
        self.assertNotIn("20171001", ps.data)

    def test_cache_data(self):
        tmp_cache_name = "tmp_cache_for_test.txt"
        if(os.path.isfile(tmp_cache_name)):
            os.remove(tmp_cache_name)

        ps = price_scrap("3035", 10)
        ps.set_today(2017, 11, 30)
        ps.cache_name = tmp_cache_name
        ps.set_data()
        ps.dbg()

        ps = price_scrap("3035", 10)
        ps.set_today(2017, 12, 1)
        ps.cache_name = tmp_cache_name
        ps.set_data()
        ps.dbg()

        self.assertEqual(ps.hit_count, 9)
        self.assertAlmostEqual(ps.data['20171201'], 61.3)
        self.assertAlmostEqual(ps.data['20171130'], 63.9)
        self.assertAlmostEqual(ps.data['20171129'], 63.0)
        self.assertAlmostEqual(ps.data['20171128'], 57.3)
        self.assertAlmostEqual(ps.data['20171127'], 58.4)
        self.assertEqual(ps.data['20171126'], None)

if __name__ == '__main__':
    logging.basicConfig(filename='test_price_scrap.log', level=logging.DEBUG)
    unittest.main()
