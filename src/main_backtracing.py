import pandas as pd
from math import *
from argparse import ArgumentParser

from pandas_ta import performance

from src.backtrace import Bot

coin = 0
buyReady = True
sellReady = True

def updateInfoGraph(dt, index, row, fee, wallet, usdt):
  myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': fee * wallet,'fiat': usdt,'coins': coin,'wallet': wallet}
  dt = dt.append(myrow,ignore_index=True)
  return dt

def backTracing(bot: Bot, usdt, buyReady, sellReady, dt, dfTest, wallet, coin, buyCondition, sellCondition, taker_fee, maker_fee):
  initalWallet = float(wallet)
  totalFees = 0.0
  nbTrades = 0

  for index, row in dfTest.iterrows():
    if buyCondition(row, bot.stochTop, bot.stochBottom, bot.stochOverSold) and usdt > 0 and buyReady == True:
      buyPrice = row['close']
      coin = usdt / buyPrice
      fee = taker_fee * coin
      coin = coin - fee
      totalFees += fee
      usdt = 0
      wallet = coin * row['close']
      #print("Buy crypto at",dfTest['close'][index],'$ the', index)

      dt = updateInfoGraph(dt, index, row, fee, wallet, usdt) 

    elif sellCondition(row, bot.stochTop, bot.stochBottom, bot.stochOverSold) and coin > 0 and sellReady == True:
      sellPrice = row['close']
      usdt = coin * sellPrice
      fee = taker_fee * usdt
      usdt = usdt - fee
      coin = 0
      totalFees += fee
      buyReady = True
      wallet = usdt
      nbTrades += 1
      print("Sell crypto at",dfTest['close'][index],'$ the', index)

      dt = updateInfoGraph(dt, index, row, fee, wallet, usdt)

  
  price = initalWallet / dfTest["close"].iloc[0] * dfTest["close"].iloc[len(dfTest)-1]
  iniClose = dfTest.iloc[0]['close']
  lastClose = dfTest.iloc[len(dfTest)-1]['close']
  holdPorcentage = ((lastClose - iniClose)/iniClose) * 100
  algoPorcentage = ((wallet - initalWallet)/initalWallet) * 100

  print("Final result: ", wallet,"$", algoPorcentage)
  print("Buy and hold: ", price,"$", holdPorcentage)

  dt['wallet'] = dt['wallet'].astype(float)
  dt['price'] = dt['price'].astype(float)

  dt[['wallet','price']].plot(subplots=True, figsize=(20,10))
  performanceHold = ((wallet - price)/ price) * 100

  return (float("{:.2f}".format(wallet)), float("{:.2f}".format(price)), float("{:.2f}".format(totalFees)), float("{:.2f}".format(performanceHold)), nbTrades)

  

def launch_analysis(bot: Bot):
    # struct of data for result
    dt = None
    dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack']) 

    # default strategy
    (_, functionBuy, functionSell) = bot.strat_array[0]

    match bot.strategy:
        case "aligator":
            (_, functionBuy, functionSell) = bot.strat_array[0]
        case "big_will":
            (_, functionBuy, functionSell) = bot.strat_array[1]
        case "ema":
            (_, functionBuy, functionSell) = bot.strat_array[2]
        case "trix":
            (_, functionBuy, functionSell) = bot.strat_array[3]
        case "true":
            (_, functionBuy, functionSell) = bot.strat_array[4]
        case "macd":
            (_, functionBuy, functionSell) = bot.strat_array[5]
        

    wallet = bot.wallet
    (botWallet, holdWallet, totalFees, performanceHold, nbTrades) = backTracing(bot, bot.wallet, buyReady, sellReady, dt, bot.df_test, wallet, coin, functionBuy, functionSell, float(bot.taker_fee) / 100, float(bot.maker_fee) / 100)

    return (bot.strategy, botWallet, holdWallet, totalFees, performanceHold, nbTrades)