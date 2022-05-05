def buy_condition_trix(row, stoch_top, stoch_bottom, stoch_over_sold):
  if row['TRIX_HISTO'] > 0 and row['STOCH_RSI'] < stoch_top:
    return True
  else:
    return False

def sell_condition_trix(row, stoch_top, stoch_bottom, stoch_over_sold):
  if row['TRIX_HISTO'] < 0 and row['STOCH_RSI'] > stoch_bottom:
    return True
  else:
    return False

def buy_condition_ema(row, stoch_top, stoch_bottom, stoch_over_sold):
  if row['EMA1p'] > row['EMA2p']:
    return True
  else:
    return False

def sell_condition_ema(row, stoch_top, stock_bottom, stoch_over_sold):
  if row['EMA2p'] > row['EMA1p']:
    return True
  else:
    return False

def buy_condition_true_strategy(row, stoch_top, stock_bottom, stoch_over_sold):
  if row['EMA28'] > row['EMA48'] and row['STOCH_RSI'] < stoch_top:
    return True
  else:
    return False

def sell_condition_true_strategy(row, stoch_top, stock_bottom, stoch_over_sold):
  if row['EMA28'] < row['EMA48'] and row['STOCH_RSI'] > stock_bottom:
    return True
  else:
    return False

def buy_condition_aligator(row, stoch_top, stock_bottom, stoch_over_sold):
  if row['EMA1'] > row['EMA2'] and row['EMA2'] > row['EMA3'] and row['EMA3'] > row['EMA4'] and row['EMA4'] > row['EMA5'] and row['EMA5'] > row['EMA6'] and row['STOCH_RSI'] < stock_bottom:
    return True
  else:
    return False

def sell_condition_aligator(row, stoch_top, stock_bottom, stoch_over_sold):
  if row['EMA6'] > row['EMA1'] and row['STOCH_RSI'] > stock_bottom:
    return True
  else:
    return False

def buy_condition_big_will(row, stoch_top, stock_bottom, stoch_over_sold):
    if (
        row['AO'] >= 0
        and row['WillR'] < -85
    ):
        return True
    else:
        return False

def sell_condition_big_will(row, stoch_top, stock_bottom, stoch_over_sold):
    if (
        (row['AO'] < 0
        and row['STOCH_RSI'] > stoch_over_sold)
        or row['WillR'] > -10
    ):
        return True
    else:
        return False