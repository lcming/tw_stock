#!/usr/bin/python3
from inst_scrap import inst_scrap
import unittest
import datetime

class test_inst_scrap(unittest.TestCase):
    fix_year = 2017
    fix_month = 12
    fix_day = 1

    def test_format_url(self):
        inss = inst_scrap("2303", 3)
        ex_url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201'
        self.assertEqual(inss.format_url("20171201"), ex_url)
        self.assertNotEqual(inss.format_url("20161001"), ex_url)

    def test_get_stock_id_idx(self):
        inss = inst_scrap("2330", 3)
        ex_url = 'http://www.twse.com.tw/fund/T86?response=json&selectType=ALL&date=20171201'
        raw_data = eval(inss.get_html_str(ex_url))
        data_part = raw_data['data']
        self.assertEqual(inss.get_stock_id_idx(data_part, "00632R"), 0)
        self.assertEqual(inss.get_stock_id_idx(data_part, "2882"), 1)
        self.assertEqual(inss.get_stock_id_idx(data_part, "2891"), 2)
        self.assertEqual(inss.get_stock_id_idx(data_part, "00637L"), 8886)

    def test_set_data(self):
        inss = inst_scrap("3035", 31)
        inss.set_today(2017, 11, 30)
        inss.set_data()
        self.assertEqual(inss.data["20171031"]['foreign_buy'], 671000)
        self.assertEqual(inss.data["20171127"]['foreign_sell'], 1682000)
        self.assertEqual(inss.data["20171129"]['total_diff'], 5041000)
        self.assertNotIn("20171030", inss.data)
        self.assertNotIn("2017111", inss.data)
        self.assertNotIn("20171126", inss.data)
        self.assertNotIn("20170929", inss.data)



if __name__ == '__main__':
    unittest.main()
