#Simple simple simple

#Regla: 20 day sma crossover 60 sma -> buy 
#       60 day sma crossover 20 sma -> sell 


from binance import Client
import constants

client = Client(constants.BINANCE_API_KEY, constants.BINANCE_SECRET_KEY)

# 1 - pull 1 hour candlesticks for the past 60 days (websockets??)

# 2 - calculate both moving averages

# 3 - if they are the same, calculate past moving averages 

# 4 - decide if its a buy or sell signal 

# 5 - place the order and set variable in position to true or false

