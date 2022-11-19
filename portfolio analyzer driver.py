import yfinance as yf
import pandas as pd
import numpy

# Place holder to simulate user input
user_input_arr = ['AAPL', 'CSX', 'PBR', 'VTWO', 'DBA']

# takes list of stock picks and creates 
# dataframe of closing prices for all of 
# the stocks for the longest possible time frame 
# (limited by smallest lifespan) (input is user stock list)
def organize_data_func(arr):
    stock_list = arr
    size = len(stock_list)-1
    time_frame_arr = []
    length_arr = []
    trimmed_data = []
    count = 0
    for i in stock_list:
        stock = yf.Ticker(i)
        data = stock.history(period="max")
        close = data['Close']
        time_frame_arr.append(close)
        count += 1
        
    for i in time_frame_arr:
        length_arr.append(len(i))
    length_arr.sort()
    smallest_period = length_arr[0]
    
    trimmed_data = []
    for i in time_frame_arr:
        trim = i.tail(smallest_period) 
        trimmed_data.append(trim)
    portfolio_dataframe = pd.concat(trimmed_data, axis=1, keys=user_input_arr)
    return portfolio_dataframe

return_table = organize_data_func(user_input_arr)

import seaborn as sb
corr = organize_data_func(user_input_arr).corr()
sb.heatmap(corr, cmap="Blues", annot=True)

period = 5
# This function takes every nth element from each stock price list
# to use as reference for rebalance. In between rebalance periods, we don't
# really care what the stock price is.


# converts dataframe columns to numpy arrays for faster calculations 
# and converts prices into returns on rebalancing time preferences.  
# (input is rebalance period)
def make_return_percentages(rebalance_period, stocks_arr, stock_table):
    table = stock_table
    rebalance_dates = table.iloc[::rebalance_period, :]
    # user_input_arr <-- list of stock tickers
    # Each column in rebalance_dates is converted to a numpy array
    # for more efficient calculations.
    price_list = []
    for i in stocks_arr:
        price_list.append(rebalance_dates[i].to_numpy())
    performance_table = []
    return_list = []
    for i in price_list:
        for j in range(len(i-1)):
            try:
                res = i[j+1]/i[j]
                return_list.append(res)
            except: 
                pass
        performance_table.append(return_list)
        return_list = []
    return performance_table

percent_table = make_return_percentages(period, user_input_arr, return_table)

# calculates 'buy and hold' returns
def buy_and_hold(weightings, roi_table):
    buy_and_hold_portfolio = weightings
    calc_table = roi_table
    index = 0
    for i in calc_table:
        for j in i:
            buy_and_hold_portfolio[index] = buy_and_hold_portfolio[index]*j
        index+=1
    #print('buy and hold: ', buy_and_hold_portfolio)
    end_val = sum(buy_and_hold_portfolio)
    #print('end value: $', format(end_val, ',.2f'))
    #print(' ')
    return end_val, buy_and_hold_portfolio

# calculates tactical rebalance returns.
def tactical_rebalance(weightings, roi_table):
    index = 0
    rebalance_portfolio = weightings
    calc_table = roi_table
    for i in calc_table:
        for j in i:
            rebalance_portfolio[index] = rebalance_portfolio[index]*j
            value = sum(rebalance_portfolio)
            rebalance_portfolio[0] = value/len(rebalance_portfolio)
            rebalance_portfolio[1] = value/len(rebalance_portfolio)
            rebalance_portfolio[2] = value/len(rebalance_portfolio)
            rebalance_portfolio[3] = value/len(rebalance_portfolio)
            rebalance_portfolio[4] = value/len(rebalance_portfolio)
        index+=1
    #print('rebalancing: ', rebalance_portfolio)
    end_val = sum(rebalance_portfolio)
    #print('end value: $', format(end_val, ',.2f'))
    return end_val, rebalance_portfolio


# need to customize weightings
# main:
portfolio_weightings = [200, 200, 200, 200, 200]
print('1: ', portfolio_weightings)
buy_and_hold_result = buy_and_hold(portfolio_weightings, percent_table)
print('2: ', portfolio_weightings)

# Need to reset portfolio weightings here before value is called again:
# portfolio_weightings should be global, but somehow it is changed once
# passed into the function... ask Daniel
portfolio_weightings = [200, 200, 200, 200, 200]
print('3: ', portfolio_weightings)
tactical_rebal_result = tactical_rebalance(portfolio_weightings, percent_table)
print('4: ', portfolio_weightings)

print('buy and hold: ', buy_and_hold_result)
print('tactical_rebal_result: ', tactical_rebal_result)
