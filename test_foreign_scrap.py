#!/usr/bin/python3
from foreign_scrap import foreign_scrap
import unittest
import logging


class test_inst_scrap(unittest.TestCase):
    fix_year = 2017
    fix_month = 12
    fix_day = 1


    def test_set_data(self):
        inss = foreign_scrap("3035", 30)
        inss.set_today(2017, 11, 30)
        inss.set_data()
        self.assertAlmostEqual(inss.data['20171020'], 22.29)
        self.assertEqual(inss.data['20171021'], None)
        self.assertAlmostEqual(inss.data['20171130'], 33.13)

if __name__ == '__main__':
    logging.basicConfig(filename='test_foreign_scrap.log', level=logging.DEBUG)
    unittest.main()
