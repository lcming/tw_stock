#!/usr/bin/python3
from stock_scrap import stock_scrap
import unittest
import logging
import os, glob


class test_scrap_template(unittest.TestCase):
    def setUp(self):
        self.fix_year = 2018
        self.fix_month = 4
        self.fix_day = 20
        self.check_points = {}

    def build_scrap(self):
        assert(0)

    def check_data(self):
        ss = self.build_scrap()
        ss.set_today(self.fix_year, self.fix_month, self.fix_day)
        ss.set_data()
        for cp in self.check_points:
            logging.info("test date %s" % cp)
            self.assertEqual(ss.data[cp], self.check_points[cp])

    def check_data_scratch(self):
        files = glob.glob('./cache_scratch/*')
        for f in files:
            os.remove(f)
        stock_scrap.scratch_mode = 1
        self.check_data()
