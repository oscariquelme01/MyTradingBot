#Regla: 20 day sma crossover 50 sma -> buy 
#       50 day sma crossover 20 sma -> sell 
from binance import Client

import datetime
import pandas as pd
import numpy as np
import constants
import websockets
import asyncio
import json
import sys

pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'

ticker = 'btcusdt'
timeframe = '1d'
url = 'wss://stream.binance.com:9443/ws/' + ticker + '@kline_'+ timeframe

client = Client(constants.BINANCE_API_KEY, constants.BINANCE_SECRET_KEY)
btc_balance = float(client.get_asset_balance(asset='BTC')['free'])
in_position = btc_balance > 0 
print(f'Already in a position?: {in_position}')


print(url)
print(datetime.datetime.now())


# 1 - pull 1 day candlesticks for the past 60 days into dataframe
candles =client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1DAY, limit=51)
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

df['Uptrend'] = np.nan
df.Uptrend.iloc[-2] = int(df.Sma20.iloc[-2] > df.Sma50.iloc[-2])

def isNewCandlestick(dataFrame, newCandleTime):
    return dataFrame.Time.iloc[-1] < newCandleTime  

def log(txt):
    dt = datetime.datetime.now()
    original_stdout = sys.stdout # Save a reference to the original standard output

    with open('log.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print('%s, %s' % (dt.isoformat(), txt))
        sys.stdout = original_stdout # Reset the standard output to its original value


async def main():
    global df, in_position
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


            else:
                df.Close.iloc[-1] = float(candle['c'])

            df.Sma20.iloc[-1] = np.mean(df.Close.iloc[-20:])
            df.Sma50.iloc[-1] = np.mean(df.Close.iloc[-50:])
            df.Uptrend.iloc[-1] = int(df.Sma20.iloc[-1] > df.Sma50.iloc[-1])

            print(df)

            #Golden cross
            if df.Uptrend.iloc[-1] > df.Uptrend.iloc[-2] and in_position == False:
                in_position = True
                eur_balance = float(client.get_asset_balance(asset='EUR')['free'])
                quantity = eur_balance/df.Close.iloc[-1]*0.95 # NO MARGIN CALLED !!
                client.order_market_buy(symbol='BTCUSDT', quantity=quantity)
                
                log(f'Buy order of {quantity} bitcoins @{df.Close.iloc[-1]} placed')

            #Death cross
            elif df.Uptrend.iloc[-1] < df.Uptrend.iloc[-2] and in_position == True:
                in_position = False
                btc_balance = float(client.get_asset_balance(asset='BTC')['free'])
                client.order_market_sell(symbol='BTCUSDT', quantity=btc_balance)
                
                log(f'Sell order of {btc_balance} bitcoins @{df.Close.iloc[-1]} placed')
            


asyncio.get_event_loop().run_until_complete(main())