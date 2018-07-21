#!/usr/bin/python3

from dist_scrap import dist_scrap
from stock_scrap import stock_scrap
import unittest
import logging
import os, glob

class test_dist_scrap(unittest.TestCase):

    def test_set_valid_dates(self):
        ds = dist_scrap("", 0)

    def test_data_scratch(self):
        files = glob.glob('./cache_scratch/*')
        for f in files:
            os.remove(f)
        stock_scrap.scratch_mode = 1
        self.test_data()

    def test_data(self):
        ds = dist_scrap("3035", 4)
        ds.set_today(2017, 11, 24)
        ds.set_data()
        try:
            self.assertEqual(ds.data["20171124"]["total_owners"], 46282)
            self.assertEqual(ds.data["20171124"]["total_shares"], 248550313)
            self.assertEqual(ds.data["20171117"]["total_owners"], 46531)
            self.assertEqual(ds.data["20171117"]["total_shares"], 248550313)
            self.assertEqual(ds.data["20171110"]["total_owners"], 47556)
            self.assertEqual(ds.data["20171110"]["total_shares"], 248550313)
            self.assertEqual(ds.data["20171103"]["total_owners"], 48292)
            self.assertEqual(ds.data["20171103"]["total_shares"], 248550313)

            self.assertEqual(ds.data["20171123"], None)
            self.assertEqual(ds.data["20171122"], None)
            self.assertEqual(ds.data["20171121"], None)
            self.assertEqual(ds.data["20171120"], None)
            self.assertEqual(ds.data["20171119"], None)
            self.assertEqual(ds.data["20171118"], None)

            some_dist = ds.data["20171124"]["dist"]
            self.assertEqual(len(some_dist), 15)
            self.assertEqual(some_dist[14]['owners'], 30)
            self.assertEqual(some_dist[14]['shares'], 110885660)
            self.assertEqual(some_dist[14]['percent'], 44.61)
        except:
            print(ds.data)
            self.fail()


if __name__ == '__main__':
    logging.basicConfig(filename='test_dist_scrap.log', level=logging.DEBUG)
    unittest.main()


