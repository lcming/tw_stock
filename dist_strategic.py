#!/usr/bin/python3
import dist_scrap
import pprint
import logging
from dist_scrap import dist_scrap

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig()
url_base = 'https://www.tdcc.com.tw/smWeb/QryStock.jsp'
ds = dist_scrap("3035", 7, url_base)
pp.pprint(ds.data)
