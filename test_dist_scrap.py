#!/usr/bin/python3

from dist_scrap import dist_scrap
from stock_scrap import stock_scrap
import unittest

class test_dist_scrap(unittest.TestCase):

    def test_pure(self):
        ss = stock_scrap("3035", 21, "")
        self.assertEqual(ss.get_pure_int(" 321, 21.000"), 32121)
        self.assertEqual(ss.get_pure_float(" 321, 21.0001"), float(32121.0001))

    def test_dist_scrap(self):
        ds = dist_scrap("3035", 21)
        ds.set_today(2017, 11, 30)
        ds.set_data()
        self.assertEqual(len(ds.data), 3)
        self.assertEqual(ds.data["20171117"]["total_owners"], 46531)
        self.assertEqual(ds.data["20171117"]["total_shares"], 248550313)
        some_dist = ds.data["20171124"]["dist"]
        self.assertEqual(len(some_dist), 15)
        self.assertEqual(some_dist[14]['owners'], 30)
        self.assertEqual(some_dist[14]['shares'], 110885660)
        self.assertEqual(some_dist[14]['percent'], 44.61)

    def test_empty_date(self):
        ds = dist_scrap("3035", 21)
        ds.set_today(2017, 11, 30)
        self.assertEqual(ds.get_daily_info("20181111"), None)
        self.assertEqual(ds.get_daily_info("20171123"), None)

    def test_non_friday(self):
        import datetime
        ds = dist_scrap("3035", 21)
        ds.set_today(2017, 11, 30)
        ds.today -= datetime.timedelta(52)
        ds.set_data()
        self.assertEqual(len(ds.request_dates), len(ds.record_dates) + 1)


if __name__ == '__main__':
    unittest.main()


