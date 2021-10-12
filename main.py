import quantstats as qs
import bt
import time
qs.extend_pandas()

#################################################################### Portfolio Allocations #####################################################################
stock_choice_1 = "spy"
stock_choice_2 = "agg"
stock_choice_3 = "qqq"
stock_choice_4 = "msft"

alloc1 = 50
alloc2 = 40
alloc3 = 7
alloc4 = 3

stock_dic = {
    stock_choice_1: float(alloc1) / 100,
    stock_choice_2: float(alloc2) / 100,
    stock_choice_3: float(alloc3) / 100,
    stock_choice_4: float(alloc4) / 100,
}  





################################################################## BT STRATEGY ##################################################################
bt_start = time.time()
data = bt.get([stock_choice_1, stock_choice_2, stock_choice_3, stock_choice_4])
data = data.dropna()
# print(data)

strategy_ = bt.Strategy(
    "Custom Strategy",
    [
        bt.algos.RunQuarterly(),
        bt.algos.SelectAll(),
        bt.algos.WeighSpecified(**stock_dic),
        bt.algos.Rebalance(),
    ],
)

test = bt.Backtest(strategy_, data)
#This is backtesting object, full of multiple dataframes and dictionaries
results = bt.run(test)

#This is the series data 
portfolio_bt = results._get_series(None).rebase()
bt_end = time.time()

print("BT Took: ", bt_end - bt_start)





# print(portfolio_bt)

################################################################## QUANTSTATS STRATEGY ##################################################################
"""
Here is quantstats doing the same thing
"""

qs_start = time.time()
#Quantstats grabs more data
portfolio_qs = qs.utils.make_index(stock_dic, rebalance="1Q")
qs_end = time.time()

print("QuantStats Took: ", qs_end-qs_start)




############################################################## USING QUANTSTATS TO SHOW STATS FOR BT #####################################################

#Quantstats likes the series in a percent change way
portfolio_bt["Custom Strategy"] = portfolio_bt["Custom Strategy"].pct_change()

From = '2018-01-01'
To   = '2021-01-01'
portfolio_bt_splice = portfolio_bt.loc[From:To,:]

print(portfolio_bt_splice)

#Quantstats extends pandas (at the top) so qs can get all the stats straight from the series dataframe
print("Max Drawdown: ", portfolio_bt.max_drawdown())
print("CAGR: ", portfolio_bt.cagr())
print("Volatility: ", portfolio_bt.volatility())
print("Sharpe: ", portfolio_bt.sharpe())
print("Sortino: ", portfolio_bt.sortino())
print("Comp: ", portfolio_bt.comp())
print(portfolio_bt_splice.monthly_returns())





############################################################## ALL THE QUANTSTATS FUNCTIONS ##################################################################

# all the stats we can generate from quantstats. These work on any pandas dataframe
"""
['avg_loss',
 'avg_return',
 'avg_win',
 'best',
 'cagr',
 'calmar',
 'common_sense_ratio',
 'comp',
 'compare',
 'compsum',
 'conditional_value_at_risk',
 'consecutive_losses',
 'consecutive_wins',
 'cpc_index',
 'cvar',
 'drawdown_details',
 'expected_return',
 'expected_shortfall',
 'exposure',
 'gain_to_pain_ratio',
 'geometric_mean',
 'ghpr',
 'greeks',
 'implied_volatility',
 'information_ratio',
 'kelly_criterion',
 'kurtosis',
 'max_drawdown',
 'monthly_returns',
 'outlier_loss_ratio',
 'outlier_win_ratio',
 'outliers',
 'payoff_ratio',
 'profit_factor',
 'profit_ratio',
 'r2',
 'r_squared',
 'rar',
 'recovery_factor',
 'remove_outliers',
 'risk_of_ruin',
 'risk_return_ratio',
 'rolling_greeks',
 'ror',
 'sharpe',
 'skew',
 'sortino',
 'adjusted_sortino',
 'tail_ratio',
 'to_drawdown_series',
 'ulcer_index',
 'ulcer_performance_index',
 'upi',
 'utils',
 'value_at_risk',
 'var',
 'volatility',
 'win_loss_ratio',
 'win_rate',
 'worst']
"""
