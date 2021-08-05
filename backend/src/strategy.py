#Simple simple simple

#Regla: 20 day sma crossover 60 sma -> buy 
#       60 day sma crossover 20 sma -> sell 


from binance import Client

import pprint as pp
import pandas as pd
import numpy as np
import constants

client = Client(constants.BINANCE_API_KEY, constants.BINANCE_SECRET_KEY)
pd.set_option("display.max_rows", None, "display.max_columns", None)

while True:
    # 1 - pull 1 hour candlesticks for the past 60 days into dataframe
    candles =client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=50)

    df = pd.DataFrame(candles, 
        columns=['Open_TimeStamp', 
                'Open', 
                'High', 
                'Low', 
                'Close', 
                'Volume',
                'Close_TimeStamp',
                'QAVolume',
                'NTrades',
                'Ign1',
                'Ign2',
                'Ign3'])

    df.drop(labels= ['Volume','Close_TimeStamp','QAVolume','NTrades','Ign1','Ign2','Ign3'], axis=1, inplace= True)

    # 2 - calculate both moving averages

    df['Sma20'] = df.Close.rolling(window = 20).mean()
    df['Sma50'] = df.Close.rolling(window = 50).mean()

    # 3 - Calculate whether sma 20 is above or below the sma 50

    df['Signal'] = 0.0
    df['Signal'] = np.where(df['Sma20'] > df['Sma50'], 1.0, 0.0)

    # 4 - decide if its a buy or sell signal 
    prev_signal = df['Signal'].iloc[0]
    in_position = prev_signal
    for signal in df['Signal']:
        if prev_signal < signal and in_position == 0:
            print('Buy! Buy! Buy!')
        elif prev_signal > signal and in_position == 1:
            print('Sell! Sell! Sell!') 
        else:
            in_position = signal

        prev_signal = signal
    # 5 - place the order and set variable in position to true or false