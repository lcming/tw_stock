import csv
import datetime
today_str = datetime.date.today().strftime("%Y%m%d")
prev_date = ""
prev_close = 0.0
print(today_str)
source = "/mnt/c/Users/cm995/Desktop/plot_data/tw_market/fuop_all_data.csv"
temp_out = "temp.txt"
fh = open(temp_out, "w")
csv_fh = open(source)
csv_reader = csv.reader(csv_fh, delimiter=',')
line_count = 0
for row in csv_reader:
    prev_date = row[0]
    prev_close = row[4]
    line = row.join(",") + "\n"
    fh.write(line)
idx_db = eval(open("cache/index_scrap_tw_index.txt", "r").read())
op_db = eval(open("cache/op_scrap_tw_index.txt", "r").read())
for date in sorted(idx_db):
    if date > prev_date and date < date.today_str:
        #row_structure = ["date", "open", "high", "low", "close", "volume", "bid_volume", "bid_deal", "ask_volume", "ask_deal"]
        line = date
        line += ", " + str(idx_db[date]["open"])
        line += ", " + str(idx_db[date]["high"])
        line += ", " + str(idx_db[date]["low"])
        line += ", " + str(idx_db[date]["close"])
        line += ", " + str(idx_db[date]["close_deal"]["acc_volume"])
        line += ", " + "%.2f" % (idx_db[date]["close"] - prev_close)
        line += ", " + str(idx_db[date]["open_deal"]["ask_deal"])
        line += ", " + str(idx_db[date]["open_deal"]["ask_volume"])
        line += ", " + str(idx_db[date]["open_deal"]["bid_deal"])
        line += ", " + str(idx_db[date]["open_deal"]["bid_volume"])
        prev_close = idx_db[date]["close"]
        line += ", " + op_db[date]["dealer call"].join(", ")
        line += ", " + op_db[date]["dealer put"].join(", ")
        #line += ", " + op_db[date]["inst call"].join(", ")
        #line += ", " + op_db[date]["inst put"].join(", ")
        line += ", " + op_db[date]["foreign call"].join(", ")
        line += ", " + op_db[date]["foreign put"].join(", ")
