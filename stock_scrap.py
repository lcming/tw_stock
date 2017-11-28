from lxml import etree, html
from retry import retry
import urllib.request
import logging
import pprint

class stock_scrap:
    stock_id = None
    url = None
    period = None
    def __init__(self, _stock_id, _period, _url):
        self.stock_id = _stock_id
        self.period = _period
        self.url = _url
    def dbg(self):
        print("Stock: %s, url: %s" % (self.stock_id, self.url))
        print("Search dates include:"),
        for date in self.dates:
            print("%s" % date),
        print("")



class dist_scrap(stock_scrap):
    dates = []
    ranges = []
    data = {}

    def __init__(self, _stock_id, _period, _url):
        super().__init__(_stock_id, _period, _url)
        self.set_data()

    def set_dates_list(self):
        import datetime
        days_traced = 0
        release_day = 4
        d = datetime.date.today()
        while (d.weekday() != release_day):
            d -= datetime.timedelta(1)
        while (days_traced < self.period):
            self.dates.append("%s%s%s" % (d.year, d.month, d.day))
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
        for row in table_rows:
            idx = row[0].text
            if (idx != '\xa0'):
                #share_range = row[1].text
                data = {}
                #data["min"], data["max"] = self.get_min_max(share_range)
                data["owners"] = row[2].text
                data["shares"] = row[3].text
                data["percent"] = row[4].text
                day_dist.append(data)
            else:
                total_owners = row[2].text
                total_shares = row[3].text
        daily_info["dist"] = day_dist
        daily_info["owners"] = total_owners
        daily_info["shares"] = total_shares
        return daily_info

    def set_data(self):
        self.set_dates_list()
        self.set_range()
        for date in self.dates:
            self.data[date] = self.get_daily_info(date)

    def set_range(self):
        most_recent = self.dates[0]
        root = etree.HTML(self.get_html_str(self.format_url(most_recent)))
        table_rows = root.xpath("//table[@class='mt']/tbody/tr[position()>1]")
        for row in table_rows:
            idx = row[0].text
            if (idx != '\xa0'):
                self.ranges.append(row[1].text)


    def format_url(self, date):
        _url = self.url + '?SCA_DATE=' + date + '&SqlMethod=StockNo&StockNo=' + self.stock_id + '&StockName=&sub=%ACd%B8%DF'
        return _url

    @retry(urllib.error.URLError)
    def get_html_str(self, url):
        rsp = urllib.request.urlopen(url)
        return rsp.read().decode('big5')

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig()
url_base = 'https://www.tdcc.com.tw/smWeb/QryStock.jsp'
ds = dist_scrap("3035", 21, url_base)
pp.pprint(ds.data)


