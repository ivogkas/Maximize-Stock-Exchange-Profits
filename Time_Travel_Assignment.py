import pandas as pd
import os
from datetime import *
import datetime as dt
from operator import itemgetter


df_all_files = pd.DataFrame()
future_sell = []
balance = 1
virtual_today = datetime.strptime("1960-1-1", '%Y-%m-%d')
transactions = []
flag = False


def create_data_frame():
    global df_all_files
    st = ["aapl", "nvda", "amzn", "tsla", "googl", "goog", "mmm", "rok", "ba", "fb"]
    # uncomment for large
    # st = ['ba', "aapl", "nvda", "amzn", "tsla", "googl", "goog"]
    for name in st:
        df_file = pd.read_csv("Stocks/Stocks/" + name + ".us.txt")
        df_file["Company"] = name
        df_all_files = pd.concat([df_all_files, df_file])

    df_all_files = df_all_files.sort_values(by=['Date'])
    df_all_files = df_all_files.reset_index(drop=True)
    df_all_files['Date'] = pd.to_datetime(df_all_files['Date'])
    # print(df_all_files)


def search_for_buy_sell():
    global balance, virtual_today, df_all_files, flag
    # search if today is a payday
    # search for the first stock you can buy
    for index, row in df_all_files.iterrows():
        for pay in future_sell:
            if pay[0] == row["Date"]:
                balance = balance + pay[1]
                virtual_today = pay[0] + dt.timedelta(days=1)
                future_sell.remove((pay[0], pay[1]))
        dates_sell = [x[0] for x in future_sell]
        dates_buy = [(x[0]) for x in transactions]  # large: dates_buy = [(x[0],x[2]) for x in transactions]
        if row["Low"] <= balance and row["Date"] >= virtual_today and row["Volume"] > 10 and row["Date"] not in dates_sell and row["Date"] not in dates_buy:  # large: (row["Date"], row["Company"]) not in dates_buy
            buy_row = row
            flag = True
            break

    if flag == False:  # no available stocks
        return
    else:
        flag = False

    # create df for this stock
    company = buy_row["Company"]
    name = "Stocks/Stocks/" + buy_row["Company"].lower() + ".us.txt"
    df_file = pd.read_csv(name)
    df_file['Date'] = pd.to_datetime(df_file['Date'])

    # find sell_day with max revenue
    max_high = 0
    for index, row in df_file.iterrows():
        dates_sell = [x[0] for x in future_sell]
        if row["Date"] >= datetime.strptime("1995-1-1", '%Y-%m-%d'):
            dates_range = 300  # large: 20
        else:
            dates_range = 800  # large: 400
        if row["Date"] > buy_row["Date"] and row["Date"] < buy_row["Date"] + dt.timedelta(days=dates_range) and row["Volume"] > 10 and row["Date"] not in dates_buy:  # large: (row["Date"], company) not in dates_buy
            if row["High"] > max_high:
                max_high = row["High"]
                sell_row = row
                flag = True

    if flag == False:
        return

    # search for better buy_day
    min_low = buy_row["Low"]
    for index, row in df_file.iterrows():
        if row["Date"] > buy_row["Date"] and row["Date"] < sell_row["Date"] and row["Volume"] > 10 and row["Date"] not in dates_buy:  # large: (row["Date"], company) not in dates_buy
            if row["Low"] < min_low:
                min_low = row["Low"]
                buy_row = row

    # search for intra_day
    intra_day = 0
    revenue = - buy_row["Low"] + sell_row["High"]
    for index, row in df_all_files.iterrows():
        if row["Date"] > sell_row["Date"]:
            break
        if row["Date"] > buy_row["Date"] and row["Date"] < sell_row["Date"] and row["Volume"] > 10 and row["Date"] not in dates_sell and row["Date"] not in dates_buy:  # large: (row["Date"], row["Company"]) not in dates_buy
            if row["High"] - row["Open"] >= revenue and row["Open"] <= balance:
                buy_row = row
                sell_row = row
                revenue = row["High"] - row["Open"]
                company = buy_row["Company"]
                intra_day = 1
            elif row["Close"] - row["Low"] >= revenue and row["Low"] <= balance and row["Volume"] > 10 and row["Date"] not in dates_sell and row["Date"] not in dates_buy:  # large: (row["Date"], row["Company"]) not in dates_buy
                buy_row = row
                sell_row = row
                revenue = row["Close"] - row["Low"]
                company = buy_row["Company"]
                intra_day = 2
            elif row["Close"] - row["Open"] >= revenue and row["Open"] <= balance and row["Volume"] > 10 and row["Date"] not in dates_sell and row["Date"] not in dates_buy:  # large: (row["Date"], row["Company"]) not in dates_buy
                buy_row = row
                sell_row = row
                revenue = row["Close"] - row["Open"]
                company = buy_row["Company"]
                intra_day = 3
    return buy_row, sell_row, company, intra_day


def make_transaction(buy, sell, company, intra_day):
    global balance, virtual_today
    virtual_today = buy["Date"] + dt.timedelta(days=1)  # large: virtual_today = buy["Date"]
    max_buy = 0.1 * buy["Volume"]
    max_sell = 0.1 * sell["Volume"]
    max_volume = min(max_buy, max_sell)
    if intra_day == 0:  # buy-low / sell-high
        max_possible_buy = balance // buy["Low"]
        while max_possible_buy > max_volume:
            max_possible_buy -= 1
        buy_action = [buy["Date"], "buy-low", company, max_possible_buy]
        sell_action = [sell["Date"], "sell-high", company, max_possible_buy]
        balance = balance - buy["Low"] * max_possible_buy
        future_sell.append((sell["Date"], max_possible_buy * sell["High"]))

    else:  # intra day
        if intra_day == 1:  # buy-open / sell-high
            max_possible_buy = balance // buy["Open"]
            while max_possible_buy > max_volume:
                max_possible_buy -= 1
            buy_action = [buy["Date"], "buy-open", company, max_possible_buy]
            sell_action = [sell["Date"], "sell-high", company, max_possible_buy]
            balance = balance - buy["Open"] * max_possible_buy
            future_sell.append((sell["Date"], max_possible_buy * sell["High"]))
        elif intra_day == 2:  # buy-low / sell-close
            max_possible_buy = balance // buy["Low"]
            while max_possible_buy > max_volume:
                max_possible_buy -= 1
            buy_action = [buy["Date"], "buy-low", company, max_possible_buy]
            sell_action = [sell["Date"], "sell-close", company, max_possible_buy]
            balance = balance - buy["Low"] * max_possible_buy
            future_sell.append((sell["Date"], max_possible_buy * sell["Close"]))
        elif intra_day == 3:  # buy-open / sell-close
            max_possible_buy = balance // buy["Open"]
            while max_possible_buy > max_volume:
                max_possible_buy -= 1
            buy_action = [buy["Date"], "buy-open", company, max_possible_buy]
            sell_action = [sell["Date"], "sell-close", company, max_possible_buy]
            balance = balance - buy["Open"] * max_possible_buy
            future_sell.append((sell["Date"], max_possible_buy * sell["Close"]))
    # print(buy_action[0], buy_action[2])
    # print(sell_action[0], sell_action[2])
    transactions.append(buy_action)
    transactions.append(sell_action)


def create_submit_file():
    global transactions
    os.remove("test_file.txt")
    with open('test_file.txt', 'a') as the_file:
        the_file.write(str(len(transactions)) + "\n")
        for line in transactions:
            day = str(line[0]).split(" ")[0]
            action = line[1]
            company = line[2].upper()
            volume = line[3]
            str_by_line = day + " " + action + " " + company + " " + str(volume)
            the_file.write(str_by_line+"\n")


def main():
    global transactions, flag
    create_data_frame()
    while len(transactions) <= 998:
        # print(len(transactions), "transactions")
        buy_sell_pair = search_for_buy_sell()
        if flag == False:  # no more transactions
            break
        else:
            flag = False
        new_buy = buy_sell_pair[0]
        new_sell = buy_sell_pair[1]
        new_company = buy_sell_pair[2]
        new_intra_day = buy_sell_pair[3]
        make_transaction(new_buy, new_sell, new_company, new_intra_day)

    transactions = sorted(transactions, key=itemgetter(0))
    create_submit_file()


main()
