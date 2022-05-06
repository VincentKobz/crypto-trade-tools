import src.strategy.init_strategy as strat
import src.main_backtracing as main
from src.backtrace import Backtrace
from src.backtrace import Bot

def launch_backtracing(test_all, pair_name, date, inter, strategy, usdt, taker_fee, maker_fee):
    backtrace = Backtrace(date, inter, pair_name)
    
    # get all data and array of with all strategy
    (dfTest, strat_array) = strat.init_data(backtrace)
    bot = Bot(float(usdt), strategy, dfTest, taker_fee, maker_fee, strat_array)
    
    res = []
    print(test_all)
    if test_all == 'false':
        res.append(main.launch_analysis(bot))
        print('One strategy')
        return res

    print(strat_array)
    for i in range(0, len(strat_array)):
        print('All strategy')
        (bot.strategy, _, _) = strat_array[i]
        res.append(main.launch_analysis(bot))
    return res
