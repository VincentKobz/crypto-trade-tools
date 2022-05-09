import pandas as pd
from binance.client import Client
import ta
import matplotlib.pyplot as plt
import numpy as np

client = Client()

pair_name = "EGLDUSDT"
start_date = "2021-01-01"
time_interval = Client.KLINE_INTERVAL_1HOUR

klines_t = client.get_historical_klines(pair_name, time_interval, start_date)

df = pd.DataFrame(klines_t, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
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
trix_length = 8
trix_signal = 19
df['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trix_length), window=trix_length), window=trix_length)
df['TRIX_PCT'] = df["TRIX"].pct_change()*100
df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'],trix_signal)
df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']
df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=12, smooth1=3, smooth2=3)

print("Indicators loaded 100%")

stoch_top = 0.81
stoch_bottom = 0.27

df_test = df.copy()

dt = None
dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])

usdt = 100
maker_fee = 0.00019
taker_fee = 0.000665

inital_wallet = usdt
wallet = usdt
coin = 0
last_ath = 0
stop_loss = 0
take_profit = 500000
buy_ready = True
sell_ready = True

def buy_condition(row):
  if row['TRIX_HISTO'] > 0 and row['STOCH_RSI'] < stoch_top:
    return True
  else:
    return False

def sell_condition(row):
  if row['TRIX_HISTO'] < 0 and row['STOCH_RSI'] > stoch_bottom:
    return True
  else:
    return False

def update_info_graph(dt, index, row, fee, wallet):
  myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': fee * row['close'],'fiat': usdt,'coins': coin,'wallet': wallet}
  dt = dt.append(myrow,ignore_index=True)
  return dt

def back_tracing(stopLoss, take_profit, usdt, buy_ready, sell_ready, dt, df_test, wallet, coin):
  for index, row in df_test.iterrows():
    if buy_condition(row) and usdt > 0 and buy_ready == True:
      buy_price = row['close']
      coin = usdt / buy_price
      fee = taker_fee * coin
      coin = coin - fee
      usdt = 0
      wallet = coin * row['close']
      print("Buy MANA at",df_test['close'][index],'$ the', index)
      dt = update_info_graph(dt, index, row, fee, wallet)

    elif sell_condition(row) and coin > 0 and sell_ready == True:
      sellPrice = row['close']
      usdt = coin * sellPrice
      fee = taker_fee * usdt
      usdt = usdt - fee
      coin = 0
      buy_ready = True
      wallet = usdt
      print("Sell EGLD at",df_test['close'][index],'$ the', index)

      dt = update_info_graph(dt, index, row, fee, wallet)

  price = inital_wallet / df_test["close"].iloc[0] * df_test["close"].iloc[len(df_test)-1]
  init_close = df_test.iloc[0]['close']
  last_close = df_test.iloc[len(df_test)-1]['close']
  hold_percentage = ((last_close - init_close) / init_close) * 100
  algo_percentage = ((wallet - inital_wallet) / inital_wallet) * 100

  print("Final result: ", wallet,"$", algo_percentage)
  print("Buy and hold: ", price,"$", hold_percentage)
  dt[['wallet','price']].plot(subplots=True, figsize=(20,10))
  plt.show()

back_tracing(stop_loss, take_profit, usdt, buy_ready, sell_ready, dt, df_test, wallet, coin)
