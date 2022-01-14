import pandas as pd
from math import *
from argparse import ArgumentParser

from pandas_ta import performance
import src.strategy.init_strategy as strat
import src.strategy.trade_condition as trade

# DATA
stochTop = 0.81
stochBottom = 0.27
stochOverSold = 0.2

coin = 0
buyReady = True
sellReady = True

def updateInfoGraph(dt, index, row, fee, wallet, usdt):
  myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': fee * wallet,'fiat': usdt,'coins': coin,'wallet': wallet}
  dt = dt.append(myrow,ignore_index=True)
  return dt

def backTracing(usdt, buyReady, sellReady, dt, dfTest, wallet, coin, buyCondition, sellCondition, taker_fee, maker_fee):
  initalWallet = float(wallet)
  totalFees = 0.0

  for index, row in dfTest.iterrows():
    if buyCondition(row, stochTop, stochBottom, stochOverSold) and usdt > 0 and buyReady == True:
      buyPrice = row['close']
      coin = usdt / buyPrice
      fee = taker_fee * coin
      coin = coin - fee
      totalFees += fee
      usdt = 0
      wallet = coin * row['close']
      print("Buy crypto at",dfTest['close'][index],'$ the', index)

      dt = updateInfoGraph(dt, index, row, fee, wallet, usdt) 

    elif sellCondition(row, stochTop, stochBottom, stochOverSold) and coin > 0 and sellReady == True:
      sellPrice = row['close']
      usdt = coin * sellPrice
      fee = taker_fee * usdt
      usdt = usdt - fee
      coin = 0
      totalFees += fee
      buyReady = True
      wallet = usdt
      print("Sell crypto at",dfTest['close'][index],'$ the', index)

      dt = updateInfoGraph(dt, index, row, fee, wallet, usdt)

  
  price = initalWallet / dfTest["close"].iloc[0] * dfTest["close"].iloc[len(dfTest)-1]
  iniClose = dfTest.iloc[0]['close']
  lastClose = dfTest.iloc[len(dfTest)-1]['close']
  holdPorcentage = ((lastClose - iniClose)/iniClose) * 100
  algoPorcentage = ((wallet - initalWallet)/initalWallet) * 100

  print("Final result: ", wallet,"$", algoPorcentage)
  print("Buy and hold: ", price,"$", holdPorcentage)
  dt[['wallet','price']].plot(subplots=True, figsize=(20,10))
  performanceHold = ((wallet - price)/ price) * 100

  return (float("{:.2f}".format(wallet)), float("{:.2f}".format(price)), float("{:.2f}".format(totalFees)), float("{:.2f}".format(performanceHold)))

  

def launch_analysis(pair, date, inter, strategy, usdt, taker_fee, maker_fee):

    dfTest = strat.init_data(pair, date, inter)

    dt = None
    dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack']) 

    functionBuy = trade.buyConditionAligator
    functionSell = trade.sellConditionAligator
    match strategy:
        case "aligator":
            functionBuy = trade.buyConditionAligator
            functionSell = trade.sellConditionAligator
        case "trix":
            functionBuy = trade.buyConditionTrix
            functionSell = trade.sellConditionTrix
        case "true":
            functionBuy = trade.buyConditionTrueStrategy
            functionSell = trade.sellConditionTrueStrategy
        case "ema":
            functionBuy = trade.buyConditionEMA
            functionSell = trade.sellConditionEMA
        case "big_will":
            functionBuy = trade.buyConditionBigWill
            functionSell = trade.sellConditionBigWill

    wallet = usdt
    (botWallet, holdWallet, totalFees, performanceHold) = backTracing(int(usdt), buyReady, sellReady, dt, dfTest, wallet, coin, functionBuy, functionSell, float(taker_fee) / 100, float(maker_fee) / 100)
    return (botWallet, holdWallet, totalFees, performanceHold)