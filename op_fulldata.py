#!/usr/bin/env python
# coding: utf-8

# In[103]:


import pandas as pd
path = "/mnt/c/Users/cm995/Desktop/plot_data/tw_market/fuop_all_data.csv"
df = pd.read_csv(path, index_col=0)
#print(df)


# In[68]:


from index_scrap import *
from op_scrap import *
from fu_scrap import *
from op_close_scrap import *


# In[72]:


import datetime
#last_trade_date = str(int(df.index[-1]))
last_trade_date = "20170103"
today = (datetime.date.today()-datetime.timedelta(1)).strftime('%Y%m%d')
print(last_trade_date)
print(today)


# In[70]:


fs = index_scrap(600)
#fs.set_stop_date(last_trade_date)
fs.set_data()
fs = op_scrap(600)
#fs.set_stop_date(last_trade_date)
fs.set_data()
fs = fu_scrap(600)
#fs.set_stop_date(last_trade_date)
fs.set_data()
fs = op_close_scrap(600)
#fs.set_stop_date(last_trade_date)
fs.set_data()


# In[81]:


rng = pd.date_range(start=last_trade_date, end=today,freq='D',closed=None)
print(rng)


# In[74]:


def cvtTS(ts):
    y = str(ts.year)
    m = str(ts.month)
    if len(m) == 1:
        m = "0" + m
    d = str(ts.day)
    if len(d) == 1:
        d = "0" + d
    return y + m + d


# In[86]:


idx_db = eval(open("cache/index_scrap_tw_index.txt", "r").read())
op_db = eval(open("cache/op_scrap_tw_index.txt", "r").read())
fu_db = eval(open("cache/fu_scrap_tw_index.txt", "r").read())
op_close_db = eval(open("cache/op_close_scrap_tw_index.txt", "r").read())
dates = [cvtTS(i) for i in rng]
print(dates)
prev_date = dates.pop(0)
print(prev_date)
prev_close = idx_db[prev_date]["close"]
print(prev_close)
header = df.columns.values


# In[96]:


rows = []
idxs = []
for date in dates:
    print(date)
    if idx_db[date] is None:
        print("skip %s" % date)
        continue
    row = []
    #row.append(date)
    row.append(str(idx_db[date]["open"]))
    row.append(str(idx_db[date]["high"]))
    row.append(str(idx_db[date]["low"]))
    row.append(str(idx_db[date]["close"]))
    row.append(str(idx_db[date]["close_deal"]["acc_volume"]))
    row.append("%.2f" % (idx_db[date]["close"] - prev_close))
    row.append(str(idx_db[date]["open_deal"]["ask_deal"]))
    row.append(str(idx_db[date]["open_deal"]["ask_volume"]))
    row.append(str(idx_db[date]["open_deal"]["bid_deal"]))
    row.append(str(idx_db[date]["open_deal"]["bid_volume"]))
    prev_close = idx_db[date]["close"]
    row += op_db[date]["dealer call"]
    row += op_db[date]["dealer put"]
    row += op_db[date]["foreign call"]
    row += op_db[date]["foreign put"]
    row += fu_db[date]["dealer"]
    row += fu_db[date]["foreign"]
    row.append(str(float(op_close_db[date]["week"]["c"])+float(op_close_db[date]["week"]["p"])))
    row.append(str(op_close_db[date]["week"]["price"]))
    row.append(str(float(op_close_db[date]["month"]["c"])+float(op_close_db[date]["month"]["p"])))
    row.append(str(op_close_db[date]["month"]["price"]))
    print(row)
    rows.append(row)
    idxs.append(date)
print(idxs)
print(rows)


# In[97]:


new_df = pd.DataFrame(data=rows, columns=header, index=idxs)
print(new_df)


# In[101]:


#merged_df = pd.concat([df,new_df])
#print(merged_df)


# In[102]:


#merged_df.to_csv(path)

