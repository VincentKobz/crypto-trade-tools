def buyConditionTrix(row, stochTop, stochBottom, stochOverSold):
  if row['TRIX_HISTO'] > 0 and row['STOCH_RSI'] < stochTop:
    return True
  else:
    return False

def sellConditionTrix(row, stochTop, stochBottom, stochOverSold):
  if row['TRIX_HISTO'] < 0 and row['STOCH_RSI'] > stochBottom:
    return True
  else:
    return False

def buyConditionEMA(row, stochTop, stochBottom, stochOverSold):
  if row['EMA1p'] > row['EMA2p']:
    return True
  else:
    return False

def sellConditionEMA(row, stochTop, stochBottom, stochOverSold):
  if row['EMA2p'] > row['EMA1p']:
    return True
  else:
    return False

def buyConditionTrueStrategy(row, stochTop, stochBottom, stochOverSold):
  if row['EMA28'] > row['EMA48'] and row['STOCH_RSI'] < stochTop:
    return True
  else:
    return False

def sellConditionTrueStrategy(row, stochTop, stochBottom, stochOverSold):
  if row['EMA28'] < row['EMA48'] and row['STOCH_RSI'] > stochBottom:
    return True
  else:
    return False

def buyConditionAligator(row, stochTop, stochBottom, stochOverSold):
  if row['EMA1'] > row['EMA2'] and row['EMA2'] > row['EMA3'] and row['EMA3'] > row['EMA4'] and row['EMA4'] > row['EMA5'] and row['EMA5'] > row['EMA6'] and row['STOCH_RSI'] < stochBottom:
    return True
  else:
    return False

def sellConditionAligator(row, stochTop, stochBottom, stochOverSold):
  if row['EMA6'] > row['EMA1'] and row['STOCH_RSI'] > stochBottom:
    return True
  else:
    return False

def buyConditionBigWill(row, stochTop, stochBottom, stochOverSold):
    if (
        row['AO'] >= 0
        and row['WillR'] < -85
    ):
        return True
    else:
        return False

def sellConditionBigWill(row, stochTop, stochBottom, stochOverSold):
    if (
        (row['AO'] < 0
        and row['STOCH_RSI'] > stochOverSold)
        or row['WillR'] > -10
    ):
        return True
    else:
        return False

def buyConditionMACD(row, stochTop, stochBottom, stochOverSold):
  if row['MACD'] > row['MACD_SIGNAL']:
    return True
  else:
    return False

def sellConditionMACD(row, stochTop, stochBottom, stochOverSold):
  if row['MACD'] < row['MACD_SIGNAL']:
    return True
  else:
    return False