import yfinance as yf
import pandas as pd
import numpy

# Place holder to simulate user input
user_input_arr = ['AAPL', 'CSX', 'PBR', 'VTWO', 'DBA']

# This loop selects the column we care about from each
# stock's data frame (closing price)
time_frame_arr = []
count = 0
for i in user_input_arr:
    stock = yf.Ticker(i)
    data = stock.history(period="max")
    close = data['Close']
    time_frame_arr.append(close)
    count += 1
    
# Determines the shortest dataframe column
# or the stock with the shorest history. Any portfolio
# analysis is limited by the stock with the shorest lifespan
length_arr = []
for i in time_frame_arr:
    length_arr.append(len(i))
length_arr.sort()
smallest_period = length_arr[0]

# Assembles columns of equivalent length for each stock,
# with the length being determined above by the stock with 
# the shortest lifespan
trimmed_data = []
for i in time_frame_arr:
    trim = i.tail(smallest_period) 
    trimmed_data.append(trim)
portfolio_dataframe = pd.concat(trimmed_data, axis=1, keys=user_input_arr)
portfolio_dataframe

# Prints a correlation heatmap which is useful information for 
# rebalance strategies
import seaborn as sb
corr = portfolio_dataframe.corr()
sb.heatmap(corr, cmap="Blues", annot=True)
#############


##################
# user input for rebalance, period.
rebalance_period = 5

# for some reason, rebalance_period adds 2 to the value when using iloc.
# so rebalance_period=7 is actually 9. That's why it is equal to '5' here.
# really strange counting issue.
# This determines the frequency of rebalance by pulling every nth element
# and storing it in 'rebalance_dates.' Iterating every 7th row gives weekly 
# rebalance, and iterating every 30th row gives monthly rebalance, etc.
rebalance_dates = portfolio_dataframe.iloc[::rebalance_period, :]
print(rebalance_dates)


# user_input_arr <-- list of stock tickers
# Each column in rebalance_dates is converted to a numpy array
# for more efficient calculations.
price_list = []
for i in user_input_arr:
    price_list.append(rebalance_dates[i].to_numpy())


# The data we have been working with hither-to-fore has been
# closing prices.  To run calculations, we calculate the growth 
# rate between each row by calculating (i+1)/i
return_table = []
return_list = []
for i in price_list:
    for j in range(len(i-1)):
        try:
            res = i[j+1]/i[j]
            return_list.append(res)
        except: 
            pass
    return_table.append(return_list)
    return_list = []
#print(len(return_table[0]))


# max time frame for user selected investments
# This tells us how long each column is in our table, which
# gives us our investment time frame.  This will be important
# later to calculate annual return in conjunction with final
# portfolio value.
investment_time_frame = len(return_table[0])
print(investment_time_frame)
print('beginning:', price_list[4][0])
print('end:', price_list[4][len(price_list[4])-1])
#####################

####################
# The portfolio weightings/dollar amounts will be selected by the user,
# but the dummy data is a portfolio of $1000 with 20% weightings in 
# 5 stocks.
##                        DBA, IPI, VTWO, PBR, CSX
buy_and_hold_portfolio = [200, 200, 200, 200, 200]


# Buy and hold loop (should be a function)
index = 0
for i in return_table:
    for j in i:
        buy_and_hold_portfolio[index] = buy_and_hold_portfolio[index]*j
    index+=1
print('buy and hold: ', buy_and_hold_portfolio)
end_val = sum(buy_and_hold_portfolio)
print('end value: $', format(end_val, ',.2f'))
print(' ')


# Rebalance portfolio with equal weightings for $1000
rebalance_portfolio = [200, 200, 200, 200, 200]

# Rebalance loop
index = 0
for i in return_table:
    for j in i:
        rebalance_portfolio[index] = rebalance_portfolio[index]*j
        ## rebalancing code:
        #-----
        value = sum(rebalance_portfolio)
        rebalance_portfolio[0] = value/len(rebalance_portfolio)
        rebalance_portfolio[1] = value/len(rebalance_portfolio)
        rebalance_portfolio[2] = value/len(rebalance_portfolio)
        rebalance_portfolio[3] = value/len(rebalance_portfolio)
        rebalance_portfolio[4] = value/len(rebalance_portfolio)
        #-----
    index+=1
print('rebalancing: ', rebalance_portfolio)
end_val = sum(rebalance_portfolio)
print('end value: $', format(end_val, ',.2f'))
###############