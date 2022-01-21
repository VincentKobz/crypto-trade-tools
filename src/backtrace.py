class backtrace:
    hold_wallet = 0
    
    def __init__(self, wallet, strategy, date, test_all, maker_fee, taker_fee):
        self.wallet = wallet
        self.strategy = strategy
        self.date = date
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.test_all = test_all