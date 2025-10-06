import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv("/mnt/c/Users/leoho/Downloads/Solana_daily_data_2018_2024.csv")
print(df.tail())

# Check

def momentum(data, short_period, long_period):
    data['short_ma'] = data['Close'].rolling(short_period).mean()
    data['long_ma'] = data['Close'].rolling(long_period).mean()
    data['momentum'] = data['short_ma'] - data['long_ma']
    
def generate_signals(data):
    data['signal'] = 0
    data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1 #buy signal
    data.loc[data['short_ma'] < data['long_ma'], 'signal'] = -1 #sell signal

def run_portfolios(data, money):
    #Assumes no short selling
    data['curr_val'] = 0.0
    position = 0
    for i in range(len(data)):
        data.loc[i, 'curr_val'] = money + position * data['Open'][i]
        if (data['signal'][i] == 1 and position <= 0):
            position = money / data['Open'][i+1]
            money = 0
        elif (data['signal'][i] == -1 and position > 0):
            money = position * data['Open'][i+1]
            position = 0

def sharpe_ratio(data, r=0.0, periods_per_year=365):
    data['returns'] = data['curr_val'].pct_change()
    excess_returns = data['returns'] - r/periods_per_year
    sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(periods_per_year)
    return sharpe

def create_charts(data):
    #Creates moving averages and price plot
    plt.figure(figsize=(14,8))
    plt.subplot(2,1,1)
    plt.plot(data['time'], data['Close'], label = 'Close', color = 'black')
    plt.plot(data['time'], data['short_ma'], label = f'Short MA ({len(data["short_ma"].dropna())})', color = 'blue')
    plt.plot(data['time'], data['long_ma'], label = f'Long MA ({len(data["long_ma"].dropna())})', color = 'red')
    for i in range(len(data)):
        if (data['signal'][i] == 1 and data['signal'][i-1] != 1):
            plt.axvline(x=data['time'][i], color='green', linestyle='--', linewidth=2, label='Buy')
        elif (data['signal'][i] == -1 and data['signal'][i-1] != -1):
            plt.axvline(x=data['time'][i], color='red', linestyle='--', linewidth=2, label='Sell')



    plt.title("Price with Moving Averages and Portfolio Val")
    plt.savefig("/mnt/c/Users/leoho/Documents/Code/Personal/MomentumTester/price")
    
    plt.figure(figsize=(14,8))
    plt.subplot(2,1,1)
    plt.plot(data['time'], data['curr_val'], label = 'Portfolio Value', color = 'green')
    for i in range(len(data)):
        if (data['signal'][i] == 1 and data['signal'][i-1] != 1):
            plt.axvline(x=data['time'][i], color='green', linestyle='--', linewidth=2, label='Buy')
        elif (data['signal'][i] == -1 and data['signal'][i-1] != -1):
            plt.axvline(x=data['time'][i], color='red', linestyle='--', linewidth=2, label='Sell')
    plt.savefig("/mnt/c/Users/leoho/Documents/Code/Personal/MomentumTester/portfolio")
    
    
    plt.figure(figsize=(14,8))
    plt.subplot(2,1,1)
    plt.plot(data['time'][0:300], data['curr_val'][0:300], label = 'Portfolio Value', color = 'green')
    plt.savefig("/mnt/c/Users/leoho/Documents/Code/Personal/MomentumTester/portfolio")

    



momentum(df, 10, 50)
generate_signals(df)
run_portfolios(df, 10000)
print(df.tail())
create_charts(df)
print(sharpe_ratio(df))
