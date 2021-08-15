import backtrader as bt
from myStrategy import smaCross

import data_generator as dt

print('Create new csv file?[Y/N]')
create_data = ''
while (create_data != 'Y' and create_data != 'y') and (create_data != 'N' and create_data != 'n'):
    create_data = input()


if create_data == 'Y' or create_data == 'y':
    dt.create_csv()
data = dt.create_bt_data()

cerebro = bt.Cerebro()
cerebro.broker.setcash(500000.0)
cerebro.adddata(data)
cerebro.addstrategy(smaCross)

cerebro.run()
cerebro.plot(volume=False)