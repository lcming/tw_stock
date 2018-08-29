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
        cache_web = self.load_cache_web(sgt_cache_name)
        if cache_web:
            null = None
            raw_data = eval(cache_web)
            stat = raw_data['stat']
        else:
            try:
                null = None
                web_str = self.get_html_str(url)
                raw_data = eval(web_str)
                stat = raw_data['stat']
            except SyntaxError:
                logging.debug("eval cache web syntax error, retry...")
                raw_data = None
                stat = None
        daily_info = {}
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
        elif (stat == '很抱歉，目前線上人數過多，請您稍候再試'):
            self.inval_cache_web(sgt_cache_name)
            self.set_daily_info(date)
            return
        else:
            logging.info("No trade on %s" % date)
            daily_info = None

        if cache_web is None:
            self.fill_cache_web(sgt_cache_name, web_str)
        self.data[date] = daily_info


