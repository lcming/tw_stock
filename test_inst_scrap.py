#!/usr/bin/python3
from inst_scrap import inst_scrap
from stock_scrap import stock_scrap
from test_scrap_template import test_scrap_template
import unittest
import logging
import os, glob


class test_inst_scrap(test_scrap_template):

    def setUp(self):
        super().setUp()
        self.check_points = {'20180413': {'invest_buy': 0, 'invest_sell': 1000, 'dealer_sell_hedge': 68000, 'foreign_dealer_sell': 0, 'dealer_diff': 227000, 'foreign_sell': 420000, 'foreign_buy': 671000, 'invest_diff': -1000, 'dealer_buy_hedge': 181000, 'foreign_dealer_buy': 0, 'dealer_buy_normal': 115000, 'dealer_diff_hedge': 113000, 'total_diff': 477000, 'foreign_diff': 251000, 'dealer_sell_normal': 1000, 'invest_diff_percent': -4.023330278405242e-06, 'dealer_diff_normal': 114000,
        'foreign_dealer_diff': 0}, '20180414': None, '20180420': {'invest_buy': 0, 'invest_sell': 4000, 'dealer_sell_hedge': 270000, 'foreign_dealer_sell': 0, 'dealer_diff': -161000, 'foreign_sell': 779000, 'foreign_buy': 995000, 'invest_diff': -4000, 'dealer_buy_hedge': 55000, 'foreign_dealer_buy': 0, 'dealer_buy_normal': 56000, 'dealer_diff_hedge': -215000, 'total_diff': 51000, 'foreign_diff': 216000, 'dealer_sell_normal': 2000, 'invest_diff_percent': -1.6093321113620967e-05,
        'dealer_diff_normal': 54000, 'foreign_dealer_diff': 0}, '20180415': None, '20180417': {'invest_buy': 50000, 'invest_sell': 0, 'dealer_sell_hedge': 159000, 'foreign_dealer_sell': 0, 'dealer_diff': -64000, 'foreign_sell': 514128, 'foreign_buy': 1061000, 'invest_diff': 50000, 'dealer_buy_hedge': 118000, 'foreign_dealer_buy': 0, 'dealer_buy_normal': 12000, 'dealer_diff_hedge': -41000, 'total_diff': 532872, 'foreign_diff': 546872, 'dealer_sell_normal': 35000, 'invest_diff_percent':
        0.0002011665139202621, 'dealer_diff_normal': -23000, 'foreign_dealer_diff': 0}, '20180419': {'invest_buy': 0, 'invest_sell': 150000, 'dealer_sell_hedge': 72000, 'foreign_dealer_sell': 0, 'dealer_diff': 286000, 'foreign_sell': 324000, 'foreign_buy': 1929000, 'invest_diff': -150000, 'dealer_buy_hedge': 391000, 'foreign_dealer_buy': 0, 'dealer_buy_normal': 29000, 'dealer_diff_hedge': 319000, 'total_diff': 1741000, 'foreign_diff': 1605000, 'dealer_sell_normal': 62000,
        'invest_diff_percent': -0.0006034995417607863, 'dealer_diff_normal': -33000, 'foreign_dealer_diff': 0}, '20180416': {'invest_buy': 0, 'invest_sell': 0, 'dealer_sell_hedge': 98000, 'foreign_dealer_sell': 0, 'dealer_diff': 272000, 'foreign_sell': 319000, 'foreign_buy': 855000, 'invest_diff': 0, 'dealer_buy_hedge': 350000, 'foreign_dealer_buy': 0, 'dealer_buy_normal': 89000, 'dealer_diff_hedge': 252000, 'total_diff': 808000, 'foreign_diff': 536000, 'dealer_sell_normal':
        69000, 'invest_diff_percent': 0.0, 'dealer_diff_normal': 20000, 'foreign_dealer_diff': 0}, '20180418': {'invest_buy': 0, 'invest_sell': 50000, 'dealer_sell_hedge': 210000, 'foreign_dealer_sell': 0, 'dealer_diff': 6000, 'foreign_sell': 707964, 'foreign_buy': 1688000, 'invest_diff': -50000, 'dealer_buy_hedge': 73000, 'foreign_dealer_buy': 0, 'dealer_buy_normal': 151000, 'dealer_diff_hedge': -137000, 'total_diff': 936036, 'foreign_diff': 980036, 'dealer_sell_normal':
        8000, 'invest_diff_percent': -0.0002011665139202621, 'dealer_diff_normal': 143000, 'foreign_dealer_diff': 0}}

    def build_scrap(self):
        ss = inst_scrap("3035", 6)
        return ss

    def test_data(self):
        super().check_data()

    def test_data_scratch(self):
        super().check_data_scratch()

if __name__ == '__main__':
    logging.basicConfig(filename='test_inst_scrap.log', level=logging.DEBUG)
    unittest.main()
