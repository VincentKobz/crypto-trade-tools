"""
module for the backtracing algorithm
"""
import pandas as pd
from src.backtrace import Bot

class BackTrace:
    """
    BackTrace class: launch the backtracing algorithm on the bot
    """
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])

        match bot.strategy:
            case "aligator":
                (_, function_buy, function_sell) = bot.strat_array[0]
            case "big_will":
                (_, function_buy, function_sell) = bot.strat_array[1]
            case "ema":
                (_, function_buy, function_sell) = bot.strat_array[2]
            case "trix":
                (_, function_buy, function_sell) = bot.strat_array[3]
            case "true":
                (_, function_buy, function_sell) = bot.strat_array[4]
            case "macd":
                (_, function_buy, function_sell) = bot.strat_array[5]

        self.buy_condition = function_buy
        self.sell_condition = function_sell
        self.bot_wallet = 0
        self.hold_wallet = 0
        self.total_fees = 0
        self.performance_hold = 0
        self.nb_trades = 0
        self.back_tracing(float(bot.taker_fee) / 100)

    def update_info_graph(self, index, row, fee, wallet, usdt, coin):
        """
        Update the dataframe with the information of the backtracing algorithm
        """
        myrow = {'date': index,'position': "Buy",'price': row['close'],'frais': fee * wallet,'fiat': usdt,'coins': coin,'wallet': wallet}
        self.dt = self.dt.append(myrow,ignore_index=True)

    def back_tracing(self, taker_fee):
        """
        Compute the backtracing algorithm
        """
        inital_wallet, total_fees, usd = float(self.bot.wallet), 0.0, self.bot.wallet

        for index, row in self.bot.df_test.iterrows():
            if self.buy_condition(row, self.bot.stoch_top, self.bot.stoch_bottom, self.bot.stoch_over_sold) and usd > 0:
                self.bot.coin = usd / row['close']
                fee = taker_fee * self.bot.coin
                self.bot.coin = self.bot.coin - fee
                total_fees += fee
                usd = 0
                self.bot.wallet = self.bot.coin * row['close']
                print("Buy crypto at", self.bot.df_test['close'][index],'$ the', index)
                self.update_info_graph(index, row, fee, self.bot.wallet, usd, self.bot.coin)

            elif self.sell_condition(row, self.bot.stoch_top, self.bot.stoch_bottom, self.bot.stoch_over_sold) and self.bot.coin > 0:
                usd = self.bot.coin * row['close']
                fee = taker_fee * usd
                usd = usd - fee
                self.bot.coin = 0
                total_fees += fee
                self.bot.wallet = usd
                self.nb_trades += 1
                print("Sell crypto at", self.bot.df_test['close'][index],'$ the', index)
                self.update_info_graph(index, row, fee, self.bot.wallet, usd, self.bot.coin)

        price = inital_wallet / self.bot.df_test["close"].iloc[0] * self.bot.df_test["close"].iloc[len(self.bot.df_test) - 1]
        init_close = self.bot.df_test.iloc[0]['close']
        last_close = self.bot.df_test.iloc[len(self.bot.df_test) - 1]['close']
        hold_percentage = ((last_close - init_close) / init_close) * 100
        algo_percentage = ((self.bot.wallet - inital_wallet) / inital_wallet) * 100

        self.dt['wallet'] = self.dt['wallet'].astype(float)
        self.dt['price'] = self.dt['price'].astype(float)
        self.dt[['wallet','price']].plot(subplots=True, figsize=(20, 10))

        print("Final result: ", self.bot.wallet,"$", algo_percentage)
        print("Buy and hold: ", price,"$", hold_percentage)

        self.performance_hold = ((self.bot.wallet - price) / price) * 100
        self.bot_wallet = self.bot.wallet
        self.hold_wallet = price
        self.total_fees = total_fees

    def result(self):
        """
        Return the result of the backtracing algorithm
        """
        return self.bot.strategy, float(f'{self.bot_wallet:.2f}'), float(f'{self.hold_wallet:.2f}'), float(f'{self.total_fees:.2f}'), float(f'{self.performance_hold:.2f}'), self.nb_trades
        