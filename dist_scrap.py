#!/usr/bin/python3

from lxml import etree, html
import logging
import pprint
from stock_scrap import stock_scrap

class dist_scrap(stock_scrap):
    ranges = []

    def __init__(self, _stock_id, _trace_len):
        _url = 'https://www.tdcc.com.tw/smWeb/QryStock.jsp'
        super().__init__(_stock_id, _trace_len, _url)

    def set_request_dates_list(self):
        import datetime
        days_traced = 0
        release_day = 4
        d = self.today
        while (d.weekday() != release_day):
            d -= datetime.timedelta(1)
        while (days_traced < self.trace_len):
            self.request_dates.append(self.get_date_string(d))
            d -= datetime.timedelta(7)
            days_traced += 7



    def get_min_max(self, share_range):
        import re
        pat = re.compile(',')
        share_range = pat.sub("", share_range)
        pat = re.compile('\d+')
        matched = pat.findall(share_range)
        if (len(matched) == 1):
            matched.append(None)
        return matched

    def get_daily_info(self, date):
        daily_info = {}
        day_dist = []
        root = etree.HTML(self.get_html_str(self.format_url(date)))
        table_rows = root.xpath("//table[@class='mt']/tbody/tr[position()>1]")
        if(table_rows):
            for row in table_rows:
                idx = row[0].text
                if (idx != '\xa0'):
                    #share_range = row[1].text
                    data = {}
                    #data["min"], data["max"] = self.get_min_max(share_range)
                    data["owners"] = self.get_pure_int(row[2].text)
                    data["shares"] = self.get_pure_int(row[3].text)
                    data["percent"] = self.get_pure_float(row[4].text)
                    day_dist.append(data)
                else:
                    total_owners = self.get_pure_int(row[2].text)
                    total_shares = self.get_pure_int(row[3].text)
            daily_info["dist"] = day_dist
            daily_info["total_owners"] = total_owners
            daily_info["total_shares"] = total_shares
        else:
            daily_info = None

        return daily_info

    def set_data(self):
        self.set_request_dates_list()
        for date in self.request_dates:
            valid_daily_info = self.get_daily_info(date)
            if(valid_daily_info):
                self.record_dates.append(date)
                self.data[date] = valid_daily_info
        if(len(self.record_dates) > 0):
            self.set_range()

    def set_range(self):
        most_recent = self.record_dates[0]
        root = etree.HTML(self.get_html_str(self.format_url(most_recent)))
        table_rows = root.xpath("//table[@class='mt']/tbody/tr[position()>1]")
        for row in table_rows:
            idx = row[0].text
            if (idx != '\xa0'):
                self.ranges.append(row[1].text)


    def format_url(self, date):
        _url = self.url + '?SCA_DATE=' + date + '&SqlMethod=StockNo&StockNo=' + self.stock_id + '&StockName=&sub=%ACd%B8%DF'
        return _url

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    logging.basicConfig()
    url_base = 'https://www.tdcc.com.tw/smWeb/QryStock.jsp'
    ds = dist_scrap("3035", 21, url_base)
    pp.pprint(ds.data)
