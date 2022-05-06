from binance.client import Client
import ta
import pandas_ta as pda
import pandas as pd
from src.backtrace import Backtrace
import src.strategy.trade_condition as tr

def init_data(bot: Backtrace):
    client = Client()
    pair_name = bot.pair
    start_date = bot.date
    print(bot.date)

    time_interval = Client.KLINE_INTERVAL_1HOUR
    print(pair_name)

    match bot.interval:
        case "1m":
            time_interval = Client.KLINE_INTERVAL_1MINUTE
        case "15m":
            time_interval = Client.KLINE_INTERVAL_15MINUTE
        case "30m":
            time_interval = Client.KLINE_INTERVAL_30MINUTE
        case "1h":
            time_interval = Client.KLINE_INTERVAL_1HOUR
        case "2h":
            time_interval = Client.KLINE_INTERVAL_2HOUR
        case "4h":
            time_interval = Client.KLINE_INTERVAL_4HOUR
        case "12h":
            time_interval = Client.KLINE_INTERVAL_12HOUR
        case "1d":
            time_interval = Client.KLINE_INTERVAL_1DAY
        case "3d":
            time_interval = Client.KLINE_INTERVAL_3DAY

    klines_t = client.get_historical_klines(pair_name, time_interval, start_date)
    

    df = pd.DataFrame(klines_t, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['open'] = pd.to_numeric(df['open'])

    df = df.set_index(df['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')
    del df['timestamp']


    df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)

    # Simple Moving Average
    df['SMA']=ta.trend.sma_indicator(df['close'], window=12)

    # Exponential Moving Average
    df['EMA1p']=ta.trend.ema_indicator(close=df['close'], window=13)
    df['EMA2p']=ta.trend.ema_indicator(close=df['close'], window=38)
    df['EMA1']=ta.trend.ema_indicator(close=df['close'], window=7)
    df['EMA2']=ta.trend.ema_indicator(close=df['close'], window=30)
    df['EMA3']=ta.trend.ema_indicator(close=df['close'], window=50)
    df['EMA4']=ta.trend.ema_indicator(close=df['close'], window=100)
    df['EMA5']=ta.trend.ema_indicator(close=df['close'], window=121)
    df['EMA6']=ta.trend.ema_indicator(close=df['close'], window=200)
    df['EMA28']=ta.trend.ema_indicator(close=df['close'], window=28)
    df['EMA48']=ta.trend.ema_indicator(close=df['close'], window=48)

    # Relative Strength Index (RSI)
    df['RSI'] =ta.momentum.rsi(close=df['close'], window=bot.rsi_length)

    # TRIX
    trix_length = bot.trix_length
    trix_signal = bot.trix_signal
    df['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trix_length), window=trix_length), window=trix_length)
    df['TRIX_PCT'] = df["TRIX"].pct_change()*100
    df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'],trix_signal)
    df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']

    # MACD
    macd = ta.trend.MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
    df['MACD'] = macd.macd()
    df['MACD_SIGNAL'] = macd.macd_signal()
    df['MACD_DIFF'] = macd.macd_diff() #Histogramme MACD

    # BigWill
    df['AO']= ta.momentum.awesome_oscillator(df['high'],df['low'],window1=bot.big_windows_1,window2=bot.big_windows_2)
    df['WillR'] = ta.momentum.williams_r(high=df['high'], low=df['low'], close=df['close'], lbp=14)

    # Stochastic RSI
    df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=12, smooth1=3, smooth2=3) #Non moyenné 
    df['STOCH_RSI_D'] = ta.momentum.stochrsi_d(close=df['close'], window=14, smooth1=3, smooth2=3) #Orange sur TradingView
    df['STOCH_RSI_K'] =ta.momentum.stochrsi_k(close=df['close'], window=14, smooth1=3, smooth2=3) #Bleu sur TradingView

    # Ichimoku
    #df['KIJUN'] = ta.trend.ichimoku_base_line(high=df['high'], low=df['low'], window1=9, window2=26)
    #df['TENKAN'] = ta.trend.ichimoku_conversion_line(high=df['high'], low=df['low'], window1=9, window2=26)
    #df['SSA'] = ta.trend.ichimoku_a(high=df['high'], low=df['low'], window1=9, window2=26)
    #df['SSB'] = ta.trend.ichimoku_b(high=df['high'], low=df['low'], window2=26, window3=52)

    # Bollinger Bands
    #bol_band = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    #df['BOL_H_BAND'] = bol_band.bollinger_hband() #Bande Supérieur
    #df['BOL_L_BAND'] = bol_band.bollinger_lband() #Bande inférieur
    #df['BOL_MAVG_BAND'] = bol_band.bollinger_mavg() #Bande moyenne

    # ADX
    #adx = ta.trend.ADXIndicator(df['high'], df['low'], df['close'], window=14) 
    #df['ADX'] = adx.adx()
    #df['ADX_NEG'] = adx.adx_neg()
    #df['ADX_POS'] = adx.adx_pos()

    # Average True Range (ATR)
    #df['ATR'] = ta.volatility.average_true_range(high=df['high'], low=df['low'], close=df['close'], window=14)

    # Super Trend
    #st_length = 10
    #st_multiplier = 3.0
    #superTrend = pda.supertrend(high=df['high'], low=df['low'], close=df['close'], length=st_length, multiplier=st_multiplier)
    #df['SUPER_TREND'] = superTrend['SUPERT_'+str(st_length)+"_"+str(st_multiplier)] #Valeur de la super trend
    #df['SUPER_TREND_DIRECTION'] = superTrend['SUPERTd_'+str(st_length)+"_"+str(st_multiplier)] #Retourne 1 si vert et -1 si rouge

    #Awesome Oscillator
    #df['AWESOME_OSCILLATOR'] = ta.momentum.awesome_oscillator(high=df['high'], low=df['low'], window1=5, window2=34)

    # Kaufman’s Adaptive Moving Average (KAMA)
    #df['KAMA'] = ta.momentum.kama(close=df['close'], window=10, pow1=2, pow2=30)
    strat_array = []
    strat_array.append(('aligator', tr.buy_condition_aligator, tr.sell_condition_aligator))
    strat_array.append(('big_will', tr.buy_condition_big_will, tr.sell_condition_big_will))
    strat_array.append(('ema', tr.buy_condition_ema, tr.sell_condition_ema))
    strat_array.append(('trix', tr.buy_condition_trix, tr.sell_condition_trix))
    strat_array.append(('true', tr.buy_condition_true_strategy, tr.sell_condition_true_strategy))
    strat_array.append(('macd', tr.buy_condition_macd, tr.sell_condition_macd))

    df_test = df.copy()

    print("Data loaded 100%")
    return (df_test, strat_array)