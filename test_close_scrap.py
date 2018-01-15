#!/usr/bin/python3
from close_scrap import close_scrap
import unittest
import logging


class test_inst_scrap(unittest.TestCase):
    fix_year = 2017
    fix_month = 12
    fix_day = 1


    def test_set_data(self):
        inss = close_scrap("3035", 30)
        inss.set_today(2017, 11, 30)
        inss.set_data()
        inss.dbg()
        self.assertEqual(inss.data['20171020'], {'deal_shares': 9898172, 'high': 46.25, 'low': 44.5, 'open': 45.2})
        self.assertEqual(inss.data['20171021'], None)
        self.assertEqual(inss.data['20171130'], {'deal_shares': 23490382, 'high': 67.8, 'low': 61.4, 'open': 62.5})

if __name__ == '__main__':
    logging.basicConfig(filename='test_close_scrap.log', level=logging.DEBUG)
    unittest.main()
