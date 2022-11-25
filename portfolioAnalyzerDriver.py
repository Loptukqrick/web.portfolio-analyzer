import yfinance as yf
import pandas as pd
import numpy


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
    
    ## for some reason, last row is all 'nan' and first row is all 'nan'
    
    #trimmed_data is a dataframe series that needs the last element removed for being 'nan'
    #print('trimmed data type: ', trimmed_data)
    portfolio_dataframe = pd.concat(trimmed_data, axis=1, keys=arr)
    
    ## for some reason the first row is all 'nan', so I'm just removing it here.
    #return_frame = portfolio_dataframe.iloc[1:, :]
    
    return portfolio_dataframe




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
        flag = 0
        for j in range(len(i)-1): 
            if j == 0:
                pass
            else:
                try:
                    res = i[j+1]/i[j]
                    return_list.append(res)
                except: 
                    print('flag: ', flag)
                    print('try except clause. except clause activated, break from loop')
                    break
                    #pass
            flag += 1
        performance_table.append(return_list)
        return_list = []
    return performance_table



# calculates 'buy and hold' returns
def buy_and_hold(weightings, roi_table):
    buy_and_hold_portfolio = weightings
    calc_table = roi_table
    #index = 0
    statement = []
    for index in range(0,len(calc_table[0])):
        value = sum(buy_and_hold_portfolio)
        statement.append(value)
        for count in range(0, len(buy_and_hold_portfolio)):
            buy_and_hold_portfolio[count] = buy_and_hold_portfolio[count]*calc_table[count][index]
    #print('buy and hold: ', buy_and_hold_portfolio)
    end_val = sum(buy_and_hold_portfolio)
    #print('end value: $', format(end_val, ',.2f'))
    #print(' ')
    return end_val, buy_and_hold_portfolio, statement

# calculates tactical rebalance returns.
def tactical_rebalance(weightings, roi_table, immutable_weightings):
    rebalance_portfolio = weightings
    calc_table = roi_table
    rebalance_results = []
#    for i in range(0,len(rebalance_portfolio)):
#        rebalance_results.append(0)
        
    statement = []
    ####################
    for index in range(0,len(calc_table[0])): #<-- number of returns
        
        for count in range(0, len(rebalance_portfolio)):
            
            rebalance_portfolio[count] = rebalance_portfolio[count]*calc_table[count][index]
        value = sum(rebalance_portfolio)
        for count in range(0, len(rebalance_portfolio)):

            rebalance_portfolio[count] = value*(immutable_weightings[count]/sum(immutable_weightings))
            
        statement.append(value)
    #print('rebalancing: ', rebalance_portfolio)
    end_val = sum(rebalance_portfolio)
    #print('end value: $', format(end_val, ',.2f'))
    return end_val, rebalance_portfolio, statement


# Place holder to simulate user input
user_input_arr = ['IPI', 'WFC', 'CMCSA', 'VTWO', 'SPHB']

benchmarks_arr = ['AMRMX', 'ANWPX', 'AMECX', 'ABNDX', 
                 'ABALX', 'AGTHX', 'VTSMX']

full_list = benchmarks_arr + user_input_arr

#                     20%       65%     10%      5%
aggressive_list = ['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']

#                   25%     40%      20%      15%
moderate_list = ['ANWPX', 'AMECX', 'ABNDX', 'ABALX']

#                     20%       10%       70%
conservative_list = ['ABALX', 'AMECX', 'ABNDX']

#          100%
index_list = ['VTSMX']

#form of example code
#print(tester.iloc[:,[0,3,4]])
# These are going to have to be extracted from the function return
aggressive_table = organize_data_func(full_list).iloc[:,[0,5,2,3]] # [0,5,2,3]
moderate_table = organize_data_func(full_list).iloc[:,[1,2,3,4]]     # [1,2,3,4]
conservative_table = organize_data_func(full_list).iloc[:,[4,2,3]] # [4,2,3]
index_table = organize_data_func(full_list).iloc[:,[6]] # [6]
return_table = organize_data_func(full_list).iloc[:,7:] #[7:]
#print(return_table)

import seaborn as sb
corr = organize_data_func(user_input_arr).corr()
sb.heatmap(corr, cmap="Blues", annot=True)

period = 5

percent_table = make_return_percentages(period, user_input_arr, return_table)
#time_frame = len(percent_table[0])
print('percent_table[0] len: ', len(percent_table[0]))
#print(percent_table)

aggressive_percent = make_return_percentages(period, aggressive_list, aggressive_table)
print('agg_percent: ', len(aggressive_percent[0]))
#print('type: ', type(aggressive_percent))
#print(aggressive_percent) # <-- 'nan' appears at end of each list in this table...

moderate_percent = make_return_percentages(period, moderate_list, moderate_table)
conservative_percent = make_return_percentages(period, conservative_list, conservative_table)
index_percent = make_return_percentages(period, index_list, index_table)


# need to customize weightings
# main:
# buy and hold
# maybe store these allocation in a global struct, then call
# upon them as needed rather than copy-and-paste
aggressive_allocation = [200, 650, 100, 50]
moderate_allocation = [250, 400, 200, 150]
conservative_allocation = [200, 100, 700]
index_allocation = [1000]

portfolio_weightings = []
for i in range(0, len(user_input_arr)):
    portfolio_weightings.append(100)
#portfolio_weightings = [200, 200, 200, 200, 200]
buy_and_hold_result = buy_and_hold(portfolio_weightings, percent_table)
bhagg = buy_and_hold(aggressive_allocation, aggressive_percent)
bhmod = buy_and_hold(moderate_allocation, moderate_percent)
bhcon = buy_and_hold(conservative_allocation, conservative_percent)
bhind = buy_and_hold(index_allocation, index_percent)


# rebalance
# need to pass in weightings for calculations so weightings stay the same

im_agg = [200, 650, 100, 50]
im_mod = [250, 400, 200, 150]
im_con = [200, 100, 700]
im_ind = [1000]

aggressive_allocation = [200, 650, 100, 50]
moderate_allocation = [250, 400, 200, 150]
conservative_allocation = [200, 100, 700]
index_allocation = [1000]
im_port = []
portfolio_weightings = []
for i in range(0, len(user_input_arr)):
    portfolio_weightings.append(100)
    im_port.append(100)
#portfolio_weightings = [200, 200, 200, 200, 200]
tactical_rebal_result = tactical_rebalance(portfolio_weightings, percent_table, im_port)
tact_agg = tactical_rebalance(aggressive_allocation, aggressive_percent, im_agg)
tact_mod = tactical_rebalance(moderate_allocation, moderate_percent, im_mod)
tact_con = tactical_rebalance(conservative_allocation, conservative_percent, im_con)
tact_ind = tactical_rebalance(index_allocation, index_percent, im_ind)


print('buy and hold: ', buy_and_hold_result[0], buy_and_hold_result[1])
#print('length: ', len(buy_and_hold_result[2]))
print('aggressive: ', bhagg[0], bhagg[1])
#print('length2: ', len(bhagg[2]))
print('moderate: ', bhmod[0], bhmod[1])
#print('length3: ', len(bhmod[2]))
print('conservative: ', bhcon[0], bhcon[1])
#print('length4: ', len(bhcon[2]))
print('index: ', bhind[0], bhind[1])
#print('length5: ', len(bhind[2]))
print(' ')
print(' ')
print('tactical_rebal_result: ', tactical_rebal_result[0], tactical_rebal_result[1])
print('aggressive: ', tact_agg[0], tact_agg[1])
print('moderate: ', tact_mod[0], tact_mod[1])
print('conservative: ', tact_con[0], tact_con[1])
print('index: ', tact_ind[0], tact_ind[1])

print('time frame: ', len(percent_table[0]))
