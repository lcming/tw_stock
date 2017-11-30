#!/usr/bin/python3
from price_scrap import price_scrap
from stock_scrap import stock_scrap
import unittest

class test_dist_scrap(unittest.TestCase):
    url_base = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG'
    def test_format_date(self):
        ps = price_scrap("2303", 30, self.url_base)
        self.assertEqual(ps.format_date("82/05/18"), "19930518")
        self.assertEqual(len(ps.dates), 2)

    def test_format_url(self):
        ps = price_scrap("2303", 3, self.url_base)
        ex_url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303'
        self.assertEqual(ps.format_url("20171001"), ex_url)
        self.assertNotEqual(ps.format_url("20161001"), ex_url)


    def test_set_data(self):
        ps = price_scrap("3035", 30, self.url_base)
        ps.set_data()
        self.assertEqual(ps.data["20171031"], 46.35)
        self.assertEqual(ps.data["20171127"], 58.4)
        self.assertEqual(ps.data["20171128"], 57.3)
        self.assertEqual(ps.data["20171129"], 63)
        self.assertIn("20171101", ps.data)
        self.assertIn("20171002", ps.data)
        self.assertNotIn("20171001", ps.data)
        self.assertNotIn("2017111", ps.data)
        self.assertNotIn("20171126", ps.data)



if __name__ == '__main__':
    unittest.main()
