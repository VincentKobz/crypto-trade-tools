import pandas
from binance.client import Client
import ta
from math import *
from argparse import ArgumentParser

client = Client()

def init_data(pair: str):
    pairName = pair
    startDate = "01 january 21"
    timeInterval = Client.KLINE_INTERVAL_1HOUR

    klinesT = client.get_historical_klines(pairName, timeInterval, startDate)

    df = pandas.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    df['close'] = pandas.to_numeric(df['close'])
    df['high'] = pandas.to_numeric(df['high'])
    df['low'] = pandas.to_numeric(df['low'])
    df['open'] = pandas.to_numeric(df['open'])

    df = df.set_index(df['timestamp'])
    df.index = pandas.to_datetime(df.index, unit='ms')
    del df['timestamp']

    df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)

    df['EMA200'] = ta.trend.ema_indicator(close=df['close'], window=200)
    trixLength = 7
    trixSignal = 15
    df['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trixLength), window=trixLength), window=trixLength)
    df['TRIX_PCT'] = df["TRIX"].pct_change()*100
    df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'],trixSignal)
    df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']

    df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=12, smooth1=3, smooth2=3)

    dfTest = None
    dt = None
    dt = pandas.DataFrame(columns = ['param1','param2', 'param3', 'result'])

    dfTest = df.copy()

    # -- If you want to run your BackTest on a specific period, uncomment the line below --
    #dfTest = df['2021-01-01':]

    return (dfTest, dt)


# -- Condition to BUY market --
def buyCondition(row, param):
  if row['TRIX_HISTO'] > 0 and row['STOCH_RSI'] < param:
    return True
  else:
    return False

# -- Condition to SELL market --  
def sellCondition(row, param):
  if row['TRIX_HISTO'] < 0 and row['STOCH_RSI'] > param:
    return True
  else:
    return False

def launch_optimization_3_parameters(dfTest, dt):
    loopI = [70,90,1]
    enumI = ceil((loopI[1] - loopI[0]) / loopI[2])

    loopJ = [10,30,1]
    enumJ = ceil((loopJ[1] - loopJ[0]) / loopJ[2])

    loopK = [12,16,1]
    enumK = ceil((loopK[1] - loopK[0]) / loopK[2])

    count = 0
    maxCount = enumI * enumJ * enumK
    for i in range(loopI[0], loopI[1], loopI[2]):
        for j in range(loopJ[0], loopJ[1], loopJ[2]):
            for k in range(loopK[0], loopK[1], loopK[2]):
                count += 1
                usdt = 100
                coin = 0

                dfTest['STOCH_RSI'] = ta.momentum.stochrsi(close=dfTest['close'], window=k, smooth1=3, smooth2=3)

                for index, row in dfTest.iterrows():
                    # Buy
                    if buyCondition(row, i/100) and usdt > 0:
                        coin = (usdt/dfTest['close'][index]) - 0.0007*(usdt/dfTest['close'][index])
                        usdt = 0
                        #print("Buy ELGD at",dfTest['close'][index],'$ the', index)

                    # Sell
                    elif sellCondition(row, j/100) and coin > 0:
                        usdt = coin*dfTest['close'][index] - (0.0007*coin*dfTest['close'][index])
                        coin = 0
                        #print("Sell EGLD at",dfTest['close'][index],'$ the', index)

                myrow = {'param1': i, 'param2': j, 'param3': k,'result': coin*dfTest.iloc[len(dfTest)-1]['close'] + usdt}
                dt = dt.append(myrow,ignore_index=True)   

    print(dt.sort_values(by=['result']))


def launch_optimization_2_parameters(dfTest, dt, param1, param2):
    loopI = [7,11,1]
    enumI = ceil((loopI[1] - loopI[0]) / loopI[2])

    loopJ = [15,25,1]
    enumJ = ceil((loopJ[1] - loopJ[0]) / loopJ[2])

    count = 0
    maxCount = enumI * enumJ
    for i in range(loopI[0], loopI[1], loopI[2]):
        for j in range(loopJ[0], loopJ[1], loopJ[2]):
              count += 1
              usdt = 100
              coin = 0

              trixLength = i
              trixSignal = j
              dfTest['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=dfTest['close'], window=trixLength), window=trixLength), window=trixLength)
              dfTest['TRIX_PCT'] = dfTest["TRIX"].pct_change()*100
              dfTest['TRIX_SIGNAL'] = ta.trend.sma_indicator(dfTest['TRIX_PCT'],trixSignal)
              dfTest['TRIX_HISTO'] = dfTest['TRIX_PCT'] - dfTest['TRIX_SIGNAL']
              dfTest['STOCH_RSI'] = ta.momentum.stochrsi(close=dfTest['close'], window=12, smooth1=3, smooth2=3)

              for index, row in dfTest.iterrows():
                  # Buy
                  if buyCondition(row, param1/100) and usdt > 0:
                      coin = (usdt/dfTest['close'][index]) - 0.0007*(usdt/dfTest['close'][index])
                      usdt = 0
                      #print("Buy ELGD at",dfTest['close'][index],'$ the', index)

                  # Sell
                  elif sellCondition(row, param2/100) and coin > 0:
                      usdt = coin*dfTest['close'][index] - (0.0007*coin*dfTest['close'][index])
                      coin = 0
                      #print("Sell EGLD at",dfTest['close'][index],'$ the', index)

              myrow = {'param1': i, 'param2': j,'result': coin*dfTest.iloc[len(dfTest)-1]['close'] + usdt}
              dt = dt.append(myrow,ignore_index=True)   

    print(dt.sort_values(by=['result']))


if __name__ == "__main__":
    parser = ArgumentParser("optimization")
    parser.add_argument("--pair", required=True, type=str)
    args = parser.parse_args()
    (dfTest, dt) = init_data(args.pair)
    launch_optimization_3_parameters(dfTest, dt)
    launch_optimization_2_parameters(dfTest, dt, 70, 29)