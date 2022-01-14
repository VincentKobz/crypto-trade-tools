import pandas as pd
from binance.client import Client
import ta
import matplotlib.pyplot as plt
import numpy as np

client = Client()

pairName = "EGLDUSDT"
startDate = "2021-01-01"
timeInterval = Client.KLINE_INTERVAL_1HOUR

klinesT = client.get_historical_klines(pairName, timeInterval, startDate)

df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
df['close'] = pd.to_numeric(df['close'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['open'] = pd.to_numeric(df['open'])

df = df.set_index(df['timestamp'])
df.index = pd.to_datetime(df.index, unit='ms')
del df['timestamp']

print("Data loaded 100%")

df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)

df['EMA200'] = ta.trend.ema_indicator(close=df['close'], window=200)
trixLength = 8
trixSignal = 19
df['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trixLength), window=trixLength), window=trixLength)
df['TRIX_PCT'] = df["TRIX"].pct_change()*100
df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'],trixSignal)
df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']
df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=12, smooth1=3, smooth2=3)

print("Indicators loaded 100%")

stochTop = 0.81
stochBottom = 0.27

dfTest = df.copy()

dt = None
dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])

usdt = 100
makerFee = 0.00019
takerFee = 0.000665

initalWallet = usdt
wallet = usdt
coin = 0
lastAth = 0
stopLoss = 0
takeProfit = 500000
buyReady = True
sellReady = True

def buyCondition(row):
  if row['TRIX_HISTO'] > 0 and row['STOCH_RSI'] < stochTop:
    return True
  else:
    return False

def sellCondition(row):
  if row['TRIX_HISTO'] < 0 and row['STOCH_RSI'] > stochBottom:
    return True
  else:
    return False

def updateInfoGraph(dt, index, row, fee, wallet):
  myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': fee * row['close'],'fiat': usdt,'coins': coin,'wallet': wallet}
  dt = dt.append(myrow,ignore_index=True)
  return dt

def backTracing(stopLoss, takeProfit, usdt, buyReady, sellReady, dt, dfTest, wallet, coin):
  for index, row in dfTest.iterrows():
    if buyCondition(row) and usdt > 0 and buyReady == True:
      buyPrice = row['close']
      coin = usdt / buyPrice
      fee = takerFee * coin
      coin = coin - fee
      usdt = 0
      wallet = coin * row['close']
      print("Buy MANA at",dfTest['close'][index],'$ the', index)

      dt = updateInfoGraph(dt, index, row, fee, wallet)
    
    #elif row['low'] < stopLoss and coin > 0:
    elif False:
      sellPrice = stopLoss
      usdt = coin * sellPrice
      fee = makerFee * usdt
      usdt = usdt - fee
      coin = 0
      buyReady = False
      wallet = usdt

      dt = updateInfoGraph(dt, index, row, fee, wallet)   

    elif sellCondition(row) and coin > 0 and sellReady == True:
      sellPrice = row['close']
      usdt = coin * sellPrice
      fee = takerFee * usdt
      usdt = usdt - fee
      coin = 0
      buyReady = True
      wallet = usdt
      print("Sell EGLD at",dfTest['close'][index],'$ the', index)

      dt = updateInfoGraph(dt, index, row, fee, wallet)

  price = initalWallet / dfTest["close"].iloc[0] * dfTest["close"].iloc[len(dfTest)-1]
  iniClose = dfTest.iloc[0]['close']
  lastClose = dfTest.iloc[len(dfTest)-1]['close']
  holdPorcentage = ((lastClose - iniClose)/iniClose) * 100
  algoPorcentage = ((wallet - initalWallet)/initalWallet) * 100

  print("Final result: ", wallet,"$", algoPorcentage)
  print("Buy and hold: ", price,"$", holdPorcentage)
  dt[['wallet','price']].plot(subplots=True, figsize=(20,10))
  plt.show()

backTracing(stopLoss, takeProfit, usdt, buyReady, sellReady, dt, dfTest, wallet, coin)
