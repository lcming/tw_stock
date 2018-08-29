from foreign_scrap import foreign_scrap
import logging

class close_scrap(foreign_scrap):

    data_base_key = ['stock_id', 'name', 'deal_shares', 'deal_count', 'deal_value', 'open', 'high', 'low', 'close']

    def __init__(self, _stock_id, _trace_len):
        super().__init__(_stock_id, _trace_len)
        self.url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&type=ALLBUT0999&_=1516023058595&'

    def parse_total_stock_daily_info(self, raw_data):
        daily_info = {}
        ok = 0
        if ('data5' in raw_data):
            data_part = raw_data['data5']
            idx = self.get_stock_id_idx(data_part, self.stock_id)
            if (idx >= 0):
                #data_base_key = ['stock_id', 'name', 'deal_shares', 'deal_count', 'deal_value', 'open', 'high', 'low', 'close']
                for i in range(2, 9):
                    key = self.data_base_key[i]
                    daily_info[key] = self.get_pure_float(data_part[idx][i])
                        #logging.warn("empty %s data <$s> for $d" % (key, str(data_part[idx][i]), self.stock_id))
                i = 2
                key = self.data_base_key[i]
                daily_info[key] = self.get_pure_int(data_part[idx][i])
            ok = 1
        return daily_info, ok


