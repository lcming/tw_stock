#!/usr/bin/python3

from dist_scrap import dist_scrap
from test_scrap_template import test_scrap_template
import unittest
import logging
import os, glob

class test_dist_scrap(test_scrap_template):

    def setUp(self):
        super().setUp()
        self.check_points = {'20180412': None, '20180405': None, '20180407': None, '20180404': None, '20180420': {'total_shares': 248550313, 'dist': [{'owners': 28105, 'shares': 4680171, 'percent': 1.88}, {'owners': 15510, 'shares': 29723643, 'percent': 11.95}, {'owners': 1876, 'shares': 13741981, 'percent': 5.52}, {'owners': 433, 'shares': 5497605, 'percent': 2.21}, {'owners': 220, 'shares': 3986651, 'percent': 1.6}, {'owners': 214, 'shares': 5490186, 'percent': 2.2}, {'owners': 116, 'shares':
        4133025, 'percent': 1.66}, {'owners': 69, 'shares': 3205691, 'percent': 1.28}, {'owners': 119, 'shares': 8417995, 'percent': 3.38}, {'owners': 77, 'shares': 11009246, 'percent': 4.42}, {'owners': 46, 'shares': 13771181, 'percent': 5.54}, {'owners': 33, 'shares': 16464522, 'percent': 6.62}, {'owners': 9, 'shares': 6045302, 'percent': 2.43}, {'owners': 7, 'shares': 6204317, 'percent': 2.49}, {'owners': 26, 'shares': 116178797, 'percent': 46.74}], 'total_owners': 46860}, '20180413':
        {'total_shares': 248550313, 'dist': [{'owners': 28174, 'shares': 4706181, 'percent': 1.89}, {'owners': 15960, 'shares': 30563378, 'percent': 12.29}, {'owners': 1923, 'shares': 14085336, 'percent': 5.66}, {'owners': 456, 'shares': 5781437, 'percent': 2.32}, {'owners': 227, 'shares': 4131932, 'percent': 1.66}, {'owners': 212, 'shares': 5425071, 'percent': 2.18}, {'owners': 122, 'shares': 4360289, 'percent': 1.75}, {'owners': 68, 'shares': 3148114, 'percent': 1.26}, {'owners': 111,
        'shares': 7909748, 'percent': 3.18}, {'owners': 85, 'shares': 12153492, 'percent': 4.88}, {'owners': 45, 'shares': 13353833, 'percent': 5.37}, {'owners': 30, 'shares': 14700501, 'percent': 5.91}, {'owners': 12, 'shares': 8088195, 'percent': 3.25}, {'owners': 5, 'shares': 4532648, 'percent': 1.82}, {'owners': 28, 'shares': 115610158, 'percent': 46.51}], 'total_owners': 47458}, '20180403': {'total_shares': 248550313, 'dist': [{'owners': 27452, 'shares': 4718957, 'percent': 1.89},
        {'owners': 15748, 'shares': 30068113, 'percent': 12.09}, {'owners': 1896, 'shares': 13874321, 'percent': 5.58}, {'owners': 433, 'shares': 5498314, 'percent': 2.21}, {'owners': 224, 'shares': 4078554, 'percent': 1.64}, {'owners': 214, 'shares': 5476385, 'percent': 2.2}, {'owners': 117, 'shares': 4170666, 'percent': 1.67}, {'owners': 68, 'shares': 3144308, 'percent': 1.26}, {'owners': 122, 'shares': 8542488, 'percent': 3.43}, {'owners': 90, 'shares': 12662872, 'percent': 5.09},
        {'owners': 48, 'shares': 14380633, 'percent': 5.78}, {'owners': 34, 'shares': 16876725, 'percent': 6.79}, {'owners': 13, 'shares': 8755955, 'percent': 3.52}, {'owners': 6, 'shares': 5188332, 'percent': 2.08}, {'owners': 27, 'shares': 111113690, 'percent': 44.7}], 'total_owners': 46492}, '20180417': None, '20180409': None, '20180410': None, '20180406': None, '20180415': None, '20180418': None, '20180411': None, '20180419': None, '20180401': None, '20180416': None, '20180414':
        None, '20180408': None, '20180331': {'total_shares': 248550313, 'dist': [{'owners': 27176, 'shares': 4726444, 'percent': 1.9}, {'owners': 15748, 'shares': 30073841, 'percent': 12.09}, {'owners': 1910, 'shares': 13978406, 'percent': 5.62}, {'owners': 434, 'shares': 5505714, 'percent': 2.21}, {'owners': 222, 'shares': 4049514, 'percent': 1.62}, {'owners': 213, 'shares': 5437990, 'percent': 2.18}, {'owners': 119, 'shares': 4243666, 'percent': 1.7}, {'owners': 69, 'shares': 3194308,
        'percent': 1.28}, {'owners': 124, 'shares': 8670423, 'percent': 3.48}, {'owners': 88, 'shares': 12380176, 'percent': 4.98}, {'owners': 48, 'shares': 14404578, 'percent': 5.79}, {'owners': 36, 'shares': 17896052, 'percent': 7.2}, {'owners': 13, 'shares': 8924863, 'percent': 3.59}, {'owners': 5, 'shares': 4505648, 'percent': 1.81}, {'owners': 26, 'shares': 110558690, 'percent': 44.48}], 'total_owners': 46231}, '20180402': None}

    def test_set_valid_dates(self):
        ds = dist_scrap("", 0)
        ds.set_valid_dates()
        assert(len(ds.valid_dates) > 10)

    def build_scrap(self):
        ss = dist_scrap("3035", 4)
        return ss

    def test_data(self):
        super().check_data()

    def test_data_scratch(self):
        super().check_data_scratch()


if __name__ == '__main__':
    logging.basicConfig(filename='test_dist_scrap.log', level=logging.DEBUG)
    unittest.main()


