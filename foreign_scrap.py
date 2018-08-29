from stock_scrap import stock_scrap
import logging

class foreign_scrap(stock_scrap):

    data_base_key = ['stock_id', 'name', 'global_id', 'total_shares', 'allow_shares', 'forein_shares', 'allow_percent', 'foreign_percent']

    def __init__(self, _stock_id, _trace_len):
        url = 'http://www.twse.com.tw/fund/MI_QFIIS?response=json&_=1515166188118&selectType=ALLBUT0999&'
        super().__init__(_stock_id, _trace_len, url)

    def format_url(self, date):
        _url = self.url + "date=" + date
        return _url

    def parse_total_stock_daily_info(self, raw_data):
        daily_info = None
        ok = 0
        if 'data' in raw_data and raw_data['data'] is not None: # 'data':[] will be treated as None
            if len(raw_data['data']) > 100:
                data_part = raw_data['data']
                idx = self.get_stock_id_idx(data_part, self.stock_id)
                if (idx >= 0):
                    i = 7
                # ['stock_id', 'name', 'global_id', 'total_shares', 'allow_shares', 'forein_shares', 'allow_percent', 'foreign_percent']
                #       0          1          2            3                4              5                 6                7
                    daily_info = self.get_pure_float(data_part[idx][i])
                else:
                    logging.info("cannot locate %s from %s" % (self.stock_id, url))
            ok = 1
            return daily_info, ok

    def get_stock_id_idx(self, stock_array, stock_id):
        idx = 0
        found = 0
        stock_id_field = 0
        for stock in stock_array:
            if (str(stock[stock_id_field]) == str(stock_id)):
                found = 1
                break
            else:
                idx += 1
        if(found == 0):
            idx = -1
        return idx


