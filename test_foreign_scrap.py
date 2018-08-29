#!/usr/bin/python3
from foreign_scrap import foreign_scrap
from test_scrap_template import test_scrap_template
import logging
import unittest


class test_foreign_scrap(test_scrap_template):

    def setUp(self):
        super().setUp()
        self.check_points = {'20180419': 29.08, '20180414': None, '20180413': 27.29, '20180420': 29.04, '20180417': 27.84, '20180416': 27.5, '20180415': None, '20180418': 28.43}

    def build_scrap(self):
        ss = foreign_scrap("3035", 6)
        return ss

    def test_data(self):
        super().check_data()

    def test_data_scratch(self):
        super().check_data_scratch()

if __name__ == '__main__':
    logging.basicConfig(filename='test_foreign_scrap.log', level=logging.DEBUG)
    unittest.main()
