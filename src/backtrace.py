class Backtrace:
    # TRIX indicator
    trixLength = 8
    trixSignal = 19

    # RSI indicator
    rsiLength = 14
    
    # Big Will indicator
    bigWindows1 = 6
    bigWindows2 = 22
    
    def __init__(self, date, interval, pair):
        self.date = date
        self.interval = interval
        self.pair = pair

class Bot:
    # Main data
    hold_wallet = 0
    total_fees = 0
    performance_hold = 0
    nb_trade = 0
    stochTop = 0.81
    stochBottom = 0.27
    stochOverSold = 0.2

    def __init__(self, wallet, strategy, df_test, taker_fee, maker_fee, strat_array):
        self.wallet = wallet
        self.strategy = strategy
        self.taker_fee = taker_fee
        self.maker_fee = maker_fee
        self.strat_array = strat_array
        self.df_test = df_test