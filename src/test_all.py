import src.strategy.init_strategy as strat
import src.main_backtracing as main

def launch_backtracing(test_all, pair_name, date, inter, strategy, usdt, taker_fee, maker_fee):
    # get all data and array of with all strategy
    (dfTest, strat_array) = strat.init_data(pair_name, date, inter)
    res = []
    print(test_all)
    if test_all == 'false':
        res.append(main.launch_analysis(strategy, usdt, taker_fee, maker_fee, dfTest, strat_array))
        print('One strategy')
        return res

    print(strat_array)
    for i in range(0, len(strat_array)):
        print('All strategy')
        (strategy_temp, _, _) = strat_array[i]
        res.append(main.launch_analysis(strategy_temp, usdt, taker_fee, maker_fee, dfTest, strat_array))
    return res
