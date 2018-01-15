from foreign_scrap import foreign_scrap
import logging

class close_scrap(foreign_scrap):

    data_base_key = ['stock_id', 'name', 'deal_shares', 'deal_count', 'deal_value', 'open', 'high', 'low', 'close']

    def __init__(self, _stock_id, _trace_len):
        super().__init__(_stock_id, _trace_len)
        self.url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&type=ALLBUT0999&_=1516023058595&'

    def set_daily_info(self, date):
        sgt_cache_name =  "./cache/" + self.__class__.__name__ + date + ".txt"
        url = self.format_url(date)
        cache_web = self.load_cache_web(sgt_cache_name, url)
        try:
            null = None
            raw_data = eval(cache_web)
        except SyntaxError:
            logging.debug("eval cache web syntax error, retry...")
            self.inval_cache_web(sgt_cache_name)
            self.set_daily_info(date)
            return
        stat = raw_data['stat']
        daily_info = {}
        if ('data5' in raw_data):
            data_part = raw_data['data5']
            idx = self.get_stock_id_idx(data_part, self.stock_id)
            if (idx >= 0):
                #data_base_key = ['stock_id', 'name', 'deal_shares', 'deal_count', 'deal_value', 'open', 'high', 'low', 'close']
                for i in range(5, 8):
                    key = self.data_base_key[i]
                    daily_info[key] = self.get_pure_float(data_part[idx][i])

                i = 2
                key = self.data_base_key[i]
                daily_info[key] = self.get_pure_int(data_part[idx][i])
        elif (stat == '很抱歉，目前線上人數過多，請您稍候再試'):
            self.inval_cache_web(sgt_cache_name)
            self.set_daily_info(date)
            return
        else:
            logging.info("No trade on %s" % date)
            daily_info = None

        self.data[date] = daily_info


