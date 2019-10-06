from gryphon.execution.strategies.base import Strategy
from decimal import Decimal
from gryphon.lib.money import Money
from gryphon.lib.exchange.consts import Consts
import gryphon.lib.metrics.quote as quote
from gryphon.lib import market_making as mm
from gryphon.lib.metrics import midpoint as midpoint_lib
from gryphon.lib.analysis.backtrader_indicators import test_indicator

import talib
import pandas as pd
# import dask.dataframe as dd

from gryphon.lib.models import datum_indicators



class MyStrat(Strategy):
    def __init__(self, db, harness, strategy_configuration, backtest_configuration):
        super(MyStrat, self).__init__(db, harness)

        self.spread = Decimal("0.01")
        self.base_volume = Money("0.5", "ETH")
        self.exchange = None
        self.slip_volume = Money("10", "ETH")
        self.volume_currency = "ETH"

        self.configure(strategy_configuration)


    def configure(self, strategy_configuration):
        super(MyStrat, self).configure(strategy_configuration) 

        self.init_configurable("spread", strategy_configuration)
        self.init_configurable("base_volume", strategy_configuration)
        self.init_configurable("exchange", strategy_configuration)

        self.init_target_exchange()


    def set_up(self):
        pass


    def init_target_exchange(self):
        self.target_exchange = self.harness.exchange_from_key(self.exchange)
        self.target_exchanges = [self.target_exchange.name]


    def signals(self, data):
        '''
        data should be a pandas dataframe with following columns names in the same order 
        columns = [datetime, open, high, low, close, volume, buy, sell, order_size]
        where buy and sell are bool series

        easy to add order_size column and change backtrader_feed_extension to pass it 
        '''

        # Add some indicators to dataframe
        data["mama"], data["fama"] = talib.MAMA(data['hl2'], fastlimit=0.5, slowlimit=0.05)
        # self.harness.log("mama : {} -- fama : {}".format(data["mama"].iloc[-2], data["fama"].iloc[-2]))

        # Add order_size to dataframe, this should be a percentage (100 = 100% of account value)
        data["order_size"] = 100

        # Create new columns in df containing buy and sell sginals
        for index, row in data.iterrows():
            if index > 2:
                if data.loc[index, "mama"] > data.loc[index, "fama"] and data.loc[index-1, "mama"] < data.loc[index-1, "fama"]:
                    data.loc[index, "buy"] = True
                    data.loc[index, "sell"] = False
                elif data.loc[index, "mama"] < data.loc[index,"fama"] and data.loc[index-1, "mama"] > data.loc[index-1, "fama"]:
                    data.loc[index, "sell"] = True
                    data.loc[index, "buy"] = False
                else:
                    data.loc[index, "buy"] = False
                    data.loc[index, "sell"] = False
            else :
                data.loc[index, "buy"] = False
                data.loc[index, "sell"] = False

        return data

   
    def tick(self, current_orders):  

        # Get orderbook 
        ob = self.target_exchange.get_orderbook()
        # print ob
        # return

        # # Get full OHLC data 
        df = self.target_exchange.get_full_ohlc(interval=240)

        signals = test_indicator.set_up(mode='execute', data=df, gryphon_strategy=MyStrat, super_kwargs=self.localslist)
        

        # Add TA-Lib indicator to dataframe
        df["mama"], df["fama"] = talib.MAMA(df["hl2"], fastlimit=0.5, slowlimit=0.2)

        # Get only OHLC for one candle
        candle = self.target_exchange.get_ohlc_from_position(240, -1)

        last_mama = df.iloc[-1]["mama"]
        last_close = df.iloc[-1]["close"]

        ticker = self.target_exchange.get_ticker()

        #! apparently for kraken, last close is much slower to update than last ticker value 
        self.harness.log("in tick - mama : {0:.2f} --- close : {1}".format(last_mama, last_close))
        self.harness.log("test idtcr : - mama : {0:.2f} --- close : {1}".format(signals.data["mama"].iloc[-1], signals.data["close"].iloc[-1]))
        self.harness.log("get candle : -                 close : {}".format(candle["close"]))
        self.harness.log('get ticker : -                 last : {}'.format(ticker["last"]))
        
        # # Test the go_long function
        # if self.go_long(data=self.df, mode='execute') is True:
        #     # self.target_exchange.limit_order(Consts.BID, bid_volume, mid_point_bid)
        #     self.harness.log('from within strategy: go long')
        # else :
        #     self.harness.log('from within strategy : stay flat')

        # Test the indicator
        # indicator = test_indicator.set_up(mode='execute', data=df, gryphon_strategy=MyStrat)



        if signals.go_long is True:
            self.harness.log('from indicator module : go long')
        elif signals.close_long is True:
            self.harness.log('from indicator module : close long')
        else:
            self.harness.log('from indicator module : stay flat')
        

        # try:
        #     datum_indicators.DatumRecorder().create(self.db)
        #     datum_indicators.DatumRecorder().record(
        #         "TA-Lib Trend", timestamp=last_ts, exchange=self.exchange,
        #         numeric_value=Decimal(last_trend.item())
        #     )
        #     self.harness.log("datum recorder success")
        # except Exception as e:
        #     self.harness.log(e)
        #     self.harness.log("datum recorder failed")
        #     pass

        # try:
        #     datum_indicators.DatumRecorder().create(self.db)
        #     datum_indicators.DatumRecorder().record(
        #         "TA-Lib MAMA", timestamp=last_ts, exchange=self.exchange, 
        #         numeric_value=Decimal(last_mama)
        #         )
        #     print "datum recorder success"
        # except Exception as e:
        #     print e
        #     print "datum recorder failed"
        #     pass
        


        # datum_mama = datum_indicators.DatumRetriever(datum_type="TA-Lib MAMA", exchange="KRAKEN_ETH_USD")
        # print datum_mama.get()
        # print datum_mama.get_pandas()


        # bid_volume, ask_volume = mm.simple_position_responsive_sizing(self.base_volume, self.position)
        # if bid_volume > 0:
        #     self.target_exchange.limit_order(Consts.BID, bid_volume, mid_point_bid)

        # print "Position :", self.position
        # print "Slippage :", slippage 
        # print "Quote :", get_quote
        # print "Mid Point Bid: ", mid_point_bid
        # print "Mid Point lib :", mid_point_fromlib
        # print "Bid Volume resp sizing :", bid_volume


        