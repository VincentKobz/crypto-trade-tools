import pandas as pd
from math import *
from argparse import ArgumentParser

from pandas_ta import performance


# DATA
stoch_top = 0.81
stoch_bottom = 0.27
stoch_over_sold = 0.2

coin, buy_ready, sell_ready = 0, True, True

def update_info_graph(dt, index, row, fee, wallet, usdt):
  myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': fee * wallet,'fiat': usdt,'coins': coin,'wallet': wallet}
  dt = dt.append(myrow,ignore_index=True)
  return dt

def back_tracing(usdt, buy_ready, sell_ready, dt, df_test, wallet, coin, buy_condition, sell_condition, taker_fee, maker_fee):
  inital_wallet = float(wallet)
  total_fees = 0.0

  for index, row in df_test.iterrows():
    if buy_condition(row, stoch_top, stoch_bottom, stoch_over_sold) and usdt > 0 and buy_ready == True:
      buy_price = row['close']
      coin = usdt / buy_price
      fee = taker_fee * coin
      coin = coin - fee
      total_fees += fee
      usdt = 0
      wallet = coin * row['close']
      #print("Buy crypto at",dfTest['close'][index],'$ the', index)

      dt = update_info_graph(dt, index, row, fee, wallet, usdt) 

    elif sell_condition(row, stoch_top, stoch_bottom, stoch_over_sold) and coin > 0 and sell_ready == True:
      sell_price = row['close']
      usdt = coin * sell_price
      fee = taker_fee * usdt
      usdt = usdt - fee
      coin = 0
      total_fees += fee
      buy_ready = True
      wallet = usdt
      #print("Sell crypto at",dfTest['close'][index],'$ the', index)

      dt = update_info_graph(dt, index, row, fee, wallet, usdt)

  
  price = inital_wallet / df_test["close"].iloc[0] * df_test["close"].iloc[len(df_test)-1]
  init_close = df_test.iloc[0]['close']
  last_close = df_test.iloc[len(df_test)-1]['close']
  hold_percentage = ((last_close - init_close) / init_close) * 100
  algo_percentage = ((wallet - inital_wallet) / inital_wallet) * 100

  print("Final result: ", wallet,"$", algo_percentage)
  print("Buy and hold: ", price,"$", hold_percentage)
  dt[['wallet','price']].plot(subplots=True, figsize=(20,10))
  performanceHold = ((wallet - price) / price) * 100

  return (float("{:.2f}".format(wallet)), float("{:.2f}".format(price)), float("{:.2f}".format(total_fees)), float("{:.2f}".format(performanceHold)))

  

def launch_analysis(strategy, usdt, taker_fee, maker_fee, dfTest, strat_array):
    # struct of data for result
    dt = None
    dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack']) 

    # default strategy
    (_, function_buy, function_sell) = strat_array[0]

    match strategy:
        case "aligator":
            (_, function_buy, function_sell) = strat_array[0]
        case "big_will":
            (_, function_buy, function_sell) = strat_array[1]
        case "ema":
            (_, function_buy, function_sell) = strat_array[2]
        case "trix":
            (_, function_buy, function_sell) = strat_array[3]
        case "true":
            (_, function_buy, function_sell) = strat_array[4]
        

    wallet = usdt
    (bot_wallet, hold_wallet, total_fees, performance_hold) = back_tracing(int(usdt), buy_ready, sell_ready, dt, dfTest, wallet, coin, function_buy, function_sell, float(taker_fee) / 100, float(maker_fee) / 100)

    return (bot_wallet, hold_wallet, total_fees, performance_hold)