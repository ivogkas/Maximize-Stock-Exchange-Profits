import pandas as pd
import os
from datetime import *
import datetime as dt
from operator import itemgetter


df_all_files = pd.DataFrame()
st = ["wmt", "jnj", "hd", "ma", "mo", "pg","xom", "jpm",  "pep", "cvx",
      "ge", "mmm", "rok", "fb", "nflx",  "mcd", "msft", 'ibm', "rcl", "amd"]

# intra_day dataframe
for name in st:
    df_file = pd.read_csv("Stocks/Stocks/" + name + ".us.txt")
    df_file["Company"] = name
    df_all_files = pd.concat([df_all_files, df_file])

df_all_files = df_all_files.sort_values(by=['Date'])
df_all_files = df_all_files.reset_index(drop=True)
df_all_files['Date'] = pd.to_datetime(df_all_files['Date'])


# best intra-day for each day and stock
list = []
for index, row in df_all_files.iterrows():
    if row["Date"] > datetime.strptime("2000-1-1", '%Y-%m-%d'):
        t1_buy = (row["Date"], - row["Open"] + row['High'], row["Company"], "buy-open", row["Volume"] * 0.1 // 1)
        t1_sell = (row["Date"], - row["Open"] + row['High'], row["Company"], "sell-high", row["Volume"] * 0.1 // 1)
        t2_buy = (row["Date"], - row["Open"] + row['Close'], row["Company"], "buy-open",  row["Volume"] * 0.1 // 1)
        t2_sell = (row["Date"], - row["Open"] + row['Close'], row["Company"], "sell-close", row["Volume"] * 0.1 // 1)
        t3_buy = (row["Date"], - row["Low"] + row['Close'], row["Company"], "buy-low", row["Volume"] * 0.1 // 1)
        t3_sell = (row["Date"], - row["Low"] + row['Close'], row["Company"], "sell-close", row["Volume"] * 0.1 // 1)

        if t1_buy[1] > t2_buy[1] and t1_buy[1] > t3_buy[1]:
            list.append(t1_buy)
            list.append(t1_sell)
        elif t2_buy[1] > t1_buy[1] and t2_buy[1] > t3_buy[1]:
            list.append(t2_buy)
            list.append(t2_sell)
        else:
            list.append(t3_buy)
            list.append(t3_sell)

list = sorted(list, key=itemgetter(0))

# intra_day file
os.remove("test_file_large.txt")
with open('test_file_large.txt', 'a') as the_file:
    the_file.write(str(len(list)) + "\n")
    for line in list:
        day = str(line[0]).split(" ")[0]
        action = line[3]
        company = line[2].upper()
        volume = line[4]
        str_by_line = day + " " + action + " " + company + " " + str(volume)
        the_file.write(str_by_line+"\n")


# main algorithm transactions
f = open('test_file.txt')
first_line = f.readline()
for line in f:
    transaction_day = datetime.strptime(line.split(" ")[0], '%Y-%m-%d')
    action = line.split(" ")[1]
    company = line.split(" ")[2]
    val = line.split(" ")[3].split("\n")[0]
    tt = (transaction_day, " ", company,  action,  str(val))
    list.append(tt)

list = sorted(list, key=itemgetter(0))

# merge intra-day and main algorithm transactions
os.remove("test_file_large.txt")
with open('test_file_large.txt', 'a') as the_file:
    the_file.write(str(len(list)) + "\n")
    for line in list:
        day = str(line[0]).split(" ")[0]
        action = line[3]
        company = line[2].upper()
        volume = line[4]
        str_by_line = day + " " + action + " " + company + " " + str(volume)
        the_file.write(str_by_line+"\n")
