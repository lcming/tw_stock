#!/usr/bin/python3
from stock_scrap import stock_scrap
import unittest
import datetime

class test_stock_scrap(unittest.TestCase):

    def test_write_cache_data(self):
        ss = stock_scrap("2303", 3, "")
        ex_url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=123456789'
        test_string = "this is a test string"
        ss.write_cache_data(test_string, ex_url)
        fh = open("./cache/http/www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=123456789")
        cache_read = fh.read()
        fh.close()
        self.assertEqual(test_string, cache_read)

    def test_url_to_cache_path(self):
        ss = stock_scrap("2303", 3, "")
        ex_url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303'
        ex_path = './cache/http/www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171001&stockNo=2303'
        self.assertEqual(ss.url_to_cache_path(ex_url), ex_path)


if __name__ == '__main__':
    unittest.main()
