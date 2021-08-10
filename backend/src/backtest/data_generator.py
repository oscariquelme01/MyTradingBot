from binance import Client

import pandas as pd
import backtrader as bt

path_to_csv = './backend/data/btc_data.csv'

def create_csv():
    client = Client()

    #Create csv file 
    data = client.get_historical_klines(
        symbol='BTCUSDT', 
        interval=Client.KLINE_INTERVAL_1DAY, 
        start_str='2019-01-01 00:00:00')
        
    df = pd.DataFrame(data)
    df.columns = ['Time', 
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
                'Ign3']
    df = df[['Time', 'Open', 'High', 'Low', 'Close']]
    df.Time = pd.to_datetime(df.Time, unit='ms')
    df.to_csv(path_to_csv, index = False, header=True)


def create_bt_data():
    data = bt.feeds.GenericCSVData(
        dataname=path_to_csv,
        dtformat=('%Y-%m-%d'),
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=-1,
        openinterest=-1
    )
    return data
    