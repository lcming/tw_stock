import csv
import datetime
from index_scrap import *
from op_scrap import *
from fu_scrap import *
from op_close_scrap import *

def write_entry(l):
    ret = ""
    for i in l:
        ret += "," + str(i)
    return ret


#today_str = datetime.date.today().strftime("%Y%m%d")
today_str = "20181229"
prev_date = "20180101"
prev_close = 0.0
test_out = "test.csv"
fh = open(test_out, "w")
#print(today_str)
#source = "fuop_all_data.csv"
#temp_out = "temp.txt"
#fh = open(temp_out, "w")
#csv_fh = open(source)
#csv_reader = csv.reader(csv_fh, delimiter=',')
#line_count = 0
#for row in csv_reader:
#    prev_date = row[0]
#    prev_close = row[4]
#    line = row.join(",") + "\n"
#    fh.write(line)

fs = index_scrap(300)
fs.set_data()
fs = op_scrap(300)
fs.set_data()
fs = fu_scrap(300)
fs.set_data()
fs = op_close_scrap(300)
fs.set_data()

idx_db = eval(open("cache/index_scrap_tw_index.txt", "r").read())
op_db = eval(open("cache/op_scrap_tw_index.txt", "r").read())
fu_db = eval(open("cache/fu_scrap_tw_index.txt", "r").read())
op_close_db = eval(open("cache/op_close_scrap_tw_index.txt", "r").read())

header = "'date','O','H','L','C','V','UD','委買張數','委買筆數','委賣張數','委賣筆數','自營cbc','自營cbv','自營csc','自營csv','自營cbsc','自營cbsv','自營cbcoi','自營cbvoi','自營cscoi','自營csvoi','自營cbscoi','自營cbsvoi','自營pbc','自營pbv','自營psc','自營psv','自營pbsc','自營pbsv','自營pbcoi','自營pbvoi','自營pscoi','自營psvoi','自營pbscoi','自營pbsvoi','外資cbc','外資cbv','外資csc','外資csv','外資cbsc','外資cbsv','外資cbcoi','外資cbvoi','外資cscoi','外資csvoi','外資cbscoi','外資cbsvoi','外資pbc','外資pbv','外資psc','外資psv','外資pbsc','外資pbsv','外資pbcoi','外資pbvoi','外資pscoi','外資psvoi','外資pbscoi','外資pbsvoi','自營bc','自營bv','自營sc','自營sv','自營bsc','自營bsv','自營oibc','自營oibv','自營oisc','自營oisv','自營oibsc','自營oibsv','外資bc','外資bv','外資sc','外資sv','外資bsc','外資bsv','外資oibc','外資oibv','外資oisc','外資oisv','外資oibsc','外資oibsv','opwcp','opwp','opmcp','opmp'\n"
fh.write(header)

for date in sorted(idx_db):
    if date > prev_date and date < today_str:
        #row_structure = ["date", "open", "high", "low", "close", "volume", "bid_volume", "bid_deal", "ask_volume", "ask_deal"]
        if idx_db[date] != None:
            try:
                line = date
                line += "," + str(idx_db[date]["open"])
                line += "," + str(idx_db[date]["high"])
                line += "," + str(idx_db[date]["low"])
                line += "," + str(idx_db[date]["close"])
                line += "," + str(idx_db[date]["close_deal"]["acc_volume"])
                line += "," + "%.2f" % (idx_db[date]["close"] - prev_close)
                line += "," + str(idx_db[date]["open_deal"]["ask_deal"])
                line += "," + str(idx_db[date]["open_deal"]["ask_volume"])
                line += "," + str(idx_db[date]["open_deal"]["bid_deal"])
                line += "," + str(idx_db[date]["open_deal"]["bid_volume"])
                prev_close = idx_db[date]["close"]
                line +=  write_entry(op_db[date]["dealer call"])
                line +=  write_entry(op_db[date]["dealer put"])
                line +=  write_entry(op_db[date]["foreign call"])
                line +=  write_entry(op_db[date]["foreign put"])
                line +=  write_entry(fu_db[date]["dealer"])
                line +=  write_entry(fu_db[date]["foreign"])
                line += "," + str(float(op_close_db[date]["week"]["c"])+float(op_close_db[date]["week"]["p"]))
                line += "," + str(op_close_db[date]["week"]["price"])
                line += "," + str(float(op_close_db[date]["month"]["c"])+float(op_close_db[date]["month"]["p"]))
                line += "," + str(op_close_db[date]["month"]["price"])
                line += "\n"
                fh.write(line)
            except Exception as e:
                import pdb
                pdb.set_trace()
                print("debug")
fh.close()
