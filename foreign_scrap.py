from inst_scrap import inst_scrap
import logging

class foreign_scrap(inst_scrap):

    data_base_key = ['stock_id', 'name', 'global_id', 'total_shares', 'allow_shares', 'forein_shares', 'allow_percent', 'foreign_percent']

    def __init__(self, _stock_id, _trace_len):
        super().__init__(_stock_id, _trace_len)
        self.url = 'http://www.twse.com.tw/fund/MI_QFIIS?response=json&_=1515166188118&selectType=ALLBUT0999&'

    def set_daily_info(self, date):
        sgt_cache_name =  self.cache_dir + self.__class__.__name__ + date + ".txt"
        url = self.format_url(date)
        cache_web = self.load_cache_web(sgt_cache_name)
        if cache_web:
            raw_data = eval(cache_web)
        else:
            try:
                web_str = self.get_html_str(url)
                raw_data = eval(web_str)
            except SyntaxError:
                logging.debug("eval cache web syntax error, retry...")
                raw_data = None
        daily_info = None
        if 'data' in raw_data and len(raw_data['data']) > 100:
            data_part = raw_data['data']
            idx = self.get_stock_id_idx(data_part, self.stock_id)
            if (idx >= 0):
                i = 7
            # ['stock_id', 'name', 'global_id', 'total_shares', 'allow_shares', 'forein_shares', 'allow_percent', 'foreign_percent']
            #       0          1          2            3                4              5                 6                7
                daily_info = self.get_pure_float(data_part[idx][i])
            else:
                logging.info("cannot locate %s from %s" % (self.stock_id, url))
        elif cache_web is None and self.daily_failed_cnt < 5:
            # we don't trust result from internet, so retry
            logging.info("retry %d times: %s" % (self.daily_failed_cnt, url))
            self.daily_failed_cnt += 1
            #self.inval_cache_web(sgt_cache_name)
            self.set_daily_info(date)
            return
        else:
            self.daily_failed_cnt = 0
            logging.info("No trade on %s" % date)
            daily_info = None

        if cache_web is None:
            self.fill_cache_web(sgt_cache_name, web_str)
        self.data[date] = daily_info

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


