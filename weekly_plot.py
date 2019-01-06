from simple_stock_filter import simple_stock_filter
import logging
import datetime

if __name__ == "__main__":
    date_str = str(datetime.date.today())
    log_name = 'weekly.log'
    logging.basicConfig(filename=log_name, level=logging.DEBUG)
    logging.debug("start...")
    volume_min = 100000
    price_min = 5.0
    price_max = 5000.0
    waived_list = []
    #waived_list = ['2614', '2208']
    for i in range(1):
        traced_weeks = i + 1
        ssf = simple_stock_filter(volume_min, price_min, price_max, traced_weeks, waived_list)
        ssf.run_viz_foreign_big()
        ssf.run_viz_inst_big()
