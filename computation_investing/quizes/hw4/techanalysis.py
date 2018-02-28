import datetime as dt
import datautils as du
import numpy as np
import pandas as pd

def calculate_bollinger_data(prices, look_back_days):
    r_mean = pd.rolling_mean(prices, look_back_days)
    r_std = pd.rolling_std(prices, look_back_days)

    ldt_timestamps = prices.index

    bollinger_array = ['bollinger']
    bollinger_data = np.empty((len(ldt_timestamps), len(bollinger_array)))
    bollinger_data.fill(np.nan)
    bollinger = pd.DataFrame(data=bollinger_data, index=ldt_timestamps, columns=bollinger_array)

    for i in range(1, len(ldt_timestamps)):
        price = prices.ix[ldt_timestamps[i]]
        rolling_mean = r_mean.ix[ldt_timestamps[i]]
        rolling_std = r_std.ix[ldt_timestamps[i]]

        bollinger.ix[ldt_timestamps[i]] = calculate_bollinger(price, rolling_mean, rolling_std)

    bollinger_data = pd.concat([prices, r_mean, r_std, bollinger], axis=1)
    bollinger_data.columns = ['closing', 'rolling_mean', 'rolling_std', 'bollinger']

    return bollinger_data

def calculate_bollinger(price, rolling_mean, rolling_std):
    return (price - rolling_mean) / (rolling_std)