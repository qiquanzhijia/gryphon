import os
import pybacktest
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt

from gryphon.lib.logger import get_logger

logger = get_logger(__name__)

def run(gryphon_strategy_class, data_path):

    '''data path is set in strategy conf file'''
    
    # Get data into a pandas dataframe
    file_extension = os.path.splitext(data_path)[1]

    if file_extension == '.csv':
        df = pd.read_csv(data_path)
        df["hl2"] = (df["high"] + df["low"]) / 2

    elif file_extension == '.h5':
        
        with pd.HDFStore(data_path) as store:
            df = store[key]

    else:
        logger.info(' only .h5 and .csv supported')

    # Get buy and sell series
    signals = gryphon_strategy_class.signals(data=df)

    signals = signals.rename(
        columns={"open" : "O",
                 "high" : "H",
                 "low" : "L",
                 "close" : "C",
                 "volume" : "V",
                })
    signals.set_index("datetime", inplace=True)

    ohlc = signals[["O", "H", "L", "C"]].copy()
    buy = cover = signals["buy"]
    sell = short = signals["sell"]

    bt = pybacktest.Backtest(locals(), gryphon_strategy_class.__class__.__name__)

    df_out_prepare = pd.concat([bt.equity, bt.trades], axis=1, join='inner')
    df_out = df_out_prepare.rename(
        columns={ 0 : "Equity",
                 "pos" : "Position",
                 "price" : "Price",
                 "vol" : "Volume",
                })

    s = '| Backtesting Strat : %s  |' % gryphon_strategy_class.__class__.__name__
    print('-' * len(s))
    print(s)
    print('-' * len(s) + '\n')
    
    logger.info("\n {}".format(df_out))   

    matplotlib.rcParams['figure.figsize'] = (15.0, 8.0)
    bt.plot_equity()
    plt.show()