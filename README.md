# Maximize-Stock-Exchange-Profits

Project for the Masters' degree course «Programming Tools and Technologies for Data Science» (2023). 

This project explores a "time-travel" trading problem, which refers to a hypothetical scenario which enables trading stocks not only on the current day but also on any chosen past date. The concept involves developing a mechanism to execute stock transactions in the past, with purpose to generate a very large revenue. 


## Problem Description
The task is to create a sequence of stock transactions that maximize profits for a given number of moves. Each move consists of a tuple (day, action, stock, quantity), where:

* day: The date of the transaction.
* action: The type of transaction, which can be "buy-low", "sell-high", "buy-open", "sell-open", "buy-close", or "sell-close".
* stock: The stock's name.
* quantity: The quantity of stocks to buy or sell.


The actions considered are:

* buy-low: Buy at the lowest price.
* sell-high: Sell at the highest price.
* buy-open, sell-open, buy-close, sell-close: Intra-day trading actions (exploit price fluctuations within a single day).

For more details, please refer to the problem.pdf file.

## Dataset
The dataset consists of historical stock price data, including opening, closing, highest, lowest prices, and volume for each stock on a daily basis. For more details, please refer to: https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs?resource=download.

## Solution
I was required to submit two sequences of stock transactions: (i) A sequence of up to 1000 transactions and (ii) a sequence of up to 1,000,000 transactions. For each sequence, I created a chart which depicts the evaluations over time.

1. For the small sequences, i achieved a profit of 13.238.781.835,441563$, with 946 transactions (see small.txt).
2. For the large sequences, i achieved a profit of 102.120.143.651,0825$, with 170.856 transactions (see large.txt).

For more details, please refer to the report.pdf file.
