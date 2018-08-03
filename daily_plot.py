from simple_stock_filter import simple_stock_filter
import logging
import datetime

if __name__ == "__main__":
    date_str = str(datetime.date.today())
    log_name = 'daily_' + date_str + '.log'
    logging.basicConfig(filename=log_name, level=logging.DEBUG)
    volume_min = 100000
    price_min = 5.0
    price_max = 5000.0
    waived_list = ['2614', '2208']
    traced_weeks = 0
    ssf = simple_stock_filter(volume_min, price_min, price_max, traced_weeks, waived_list)
    ssf.run_daily_viz_foreign_inst()
