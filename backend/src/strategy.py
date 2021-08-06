#Simple simple simple

#Regla: 20 day sma crossover 60 sma -> buy 
#       60 day sma crossover 20 sma -> sell 


from time import timezone
from binance import Client

import datetime
import pprint as pp
import pandas as pd
import numpy as np
import constants
import websockets
import asyncio
import json

pd.set_option('display.max_rows', None)

client = Client(constants.BINANCE_API_KEY, constants.BINANCE_SECRET_KEY)

ticker = 'btcusdt'
timeframe = '1h'
url = 'wss://stream.binance.com:9443/ws/' + ticker + '@kline_'+ timeframe
print(url)


# 1 - pull 1 hour candlesticks for the past 60 days into dataframe
candles =client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=50)
print(client.get_server_time())

df = pd.DataFrame(candles, 
    columns=['Time', 
            'Open', 
            'High', 
            'Low', 
            'Close', 
            'Volume',
            'Close_timestamp',
            'QAVolume',
            'NTrades',
            'Ign1',
            'Ign2',
            'Ign3'])

df.drop(labels= ['Open','High','Low','Volume','Close_timestamp','QAVolume','NTrades','Ign1','Ign2','Ign3'], axis=1, inplace= True)
df.Time = pd.to_datetime(df.Time, unit='ms')
df.Close = df['Close'].astype(float).round(decimals=2)

# 2 - calculate both moving averages

df['Sma20'] = df.Close.rolling(window = 20).mean()
df['Sma50'] = df.Close.rolling(window = 50).mean()

# 3 - Calculate whether sma 20 is above or below the sma 50

df['Signal'] = 0.0
df['Signal'] = np.where(df['Sma20'] > df['Sma50'], 1.0, 0.0)

# # 4 - decide if its a buy or sell signal 
# prev_signal = df['Signal'].iloc[0]
# in_position = prev_signal
# for signal in df['Signal']:
#     if prev_signal < signal and in_position == 0:
#         print('Buy! Buy! Buy!')
#     elif prev_signal > signal and in_position == 1:
#         print('Sell! Sell! Sell!') 
#     else:
#         in_position = signal

#     prev_signal = signal  

def isNewCandlestick(dataFrame, newCandleTime):
    print(dataFrame.Time.iloc[-1])
    print(newCandleTime)
    return dataFrame.Time.iloc[-1] < newCandleTime  

# # 5 - place the order and set variable in position to true or false
async def main():
    global df
    #Connects to binance websocket
    async with websockets.connect(url) as ws:
        while True: 
            #waits for message and appends it to dataframe
            response = await ws.recv()
            candle = json.loads(response)["k"]
            date = datetime.datetime.utcfromtimestamp(candle['t']/1000.0)
            date = date.replace(microsecond=0)
            if isNewCandlestick(df, date) == True:
                print("New candlestick received!")
                df = df.append({'Time': date, 'Close': float(candle['c']) }, ignore_index=True)
            print(df)
            

asyncio.get_event_loop().run_until_complete(main())