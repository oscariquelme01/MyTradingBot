import backtrader as bt

class smaCross(bt.Strategy):
    params = dict(
        pfast=20,  # period for the fast moving average
        pslow=50   # period for the slow moving average
    )
    def __init__(self):
        self.smaF = bt.ind.SimpleMovingAverage(period=self.params.pfast)
        self.smaS = bt.ind.SimpleMovingAverage(period=self.params.pslow)
        self.crossover = bt.ind.CrossOver(self.smaF, self.smaS)
            
    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                buy_order = self.buy(size=self.broker.get_cash()/self.data.close[0])  # enter long

        elif self.crossover < 0 and self.position:  # in the market & cross to the downside
            sell_order = self.close()  # close long position

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED/SUBMITTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Sentinel to None: new orders allowed
        self.order = None
