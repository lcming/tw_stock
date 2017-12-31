#!/usr/bin/python3

from dist_scrap import dist_scrap
from stock_scrap import stock_scrap
import unittest
import logging

class test_dist_scrap(unittest.TestCase):

    def test_dist_scrap(self):
        ds = dist_scrap("3035", 4)
        ds.set_today(2017, 11, 30)
        ds.set_data()
        self.assertEqual(ds.data["20171117"]["total_owners"], 46531)
        self.assertEqual(ds.data["20171117"]["total_shares"], 248550313)
        some_dist = ds.data["20171124"]["dist"]
        self.assertEqual(len(some_dist), 15)
        self.assertEqual(some_dist[14]['owners'], 30)
        self.assertEqual(some_dist[14]['shares'], 110885660)
        self.assertEqual(some_dist[14]['percent'], 44.61)
        ds.dbg()

    def test_empty_date(self):
        ds = dist_scrap("3035", 4)
        ds.set_today(2017, 11, 30)
        self.assertEqual(ds.get_daily_info("20181111"), None)
        self.assertEqual(ds.get_daily_info("20171123"), None)

if __name__ == '__main__':
    logging.basicConfig(filename='test_dist_scrap.log', level=logging.DEBUG)
    unittest.main()


