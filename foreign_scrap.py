from inst_scrap import inst_scrap
import logging

class foreign_scrap(inst_scrap):

    data_base_key = ['stock_id', 'name', 'global_id', 'total_shares', 'allow_shares', 'forein_shares', 'allow_percent', 'foreign_percent']

    def __init__(self, _stock_id, _trace_len):
        super().__init__(_stock_id, _trace_len)
        self.url = 'http://www.twse.com.tw/fund/MI_QFIIS?response=json&_=1515166188118&selectType=ALLBUT0999&'

    def set_daily_info(self, date):
        sgt_cache_name =  "./cache/" + self.__class__.__name__ + date + ".txt"
        url = self.format_url(date)
        cache_web = self.load_cache_web(sgt_cache_name, url)
        try:
            raw_data = eval(cache_web)
        except SyntaxError:
            logging.debug("eval cache web syntax error, retry...")
            self.inval_cache_web(sgt_cache_name)
            self.set_daily_info(date)
            return
        stat = raw_data['stat']
        daily_info = None
        if ('data' in raw_data):
            data_part = raw_data['data']
            idx = self.get_stock_id_idx(data_part, self.stock_id)
            if (idx >= 0):
                i = 7
            # ['stock_id', 'name', 'global_id', 'total_shares', 'allow_shares', 'forein_shares', 'allow_percent', 'foreign_percent']
            #       0          1          2            3                4              5                 6                7
                daily_info = self.get_pure_float(data_part[idx][i])
            else:
                logging.info("No trade on %s" % date)
                daily_info = None
        elif (stat == '很抱歉，目前線上人數過多，請您稍候再試'):
            self.inval_cache_web(sgt_cache_name)
            self.set_daily_info(date)
            return
        else:
            logging.error("error fetching inst data with url %s" )

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


