import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.parabolic_stop_and_reverse import ParabolicSAR
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2017-01-01'):pd.Timestamp('2019-01-01')]

ticker = "0005.HK"

# Parabolic SAR

psar = ParabolicSAR(df)
psar_fig = psar.plot_PSAR()
psar_fig.suptitle('HK.0005 - Parabolic SAR', fontsize=14)
psar_fig.savefig('./figures/trend/03-psar-plot')
plt.show()

signals = psar.gen_signals()
signal_fig = psar.plot_signals(signals)
signal_fig.suptitle('Parabolic SAR - Signals', fontsize=14)
signal_fig.savefig('./figures/trend/03-psar_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}%".format(value = (portfolio['total'][-1] - portfolio['total'][0])/portfolio['total'][-1]*100))
# for analysis
print("No. of trade: {value}".format(value = len(signals[signals.positions == 1])))

backtest_fig.suptitle('Parabolic SAR - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/trend/03-psar_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('Parabolic SAR - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/trend/03-psar_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))
