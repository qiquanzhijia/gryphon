import configparser
from delorean import Delorean
import pickle
import random
import termcolor as tc

from cdecimal import Decimal, InvalidOperation, ROUND_UP, ROUND_DOWN

from gryphon.lib.configurable_object import ConfigurableObject
from gryphon.lib.exchange.consts import Consts
import gryphon.lib.gryphonfury.positions as positions
from gryphon.lib.logger import get_logger
from gryphon.lib.models.datum import DatumRecorder
from gryphon.lib.models.flag import Flag
from gryphon.lib.models.order import Order
from gryphon.lib.money import Money
from gryphon.lib.session import commit_mysql_session

import os

logger = get_logger(__name__)


MIN_VOLUME_OBFUSCATION = 0.00
MAX_VOLUME_OBFUSCATION = 0.10


class Strategy(ConfigurableObject):
    def __init__(self, db, harness=None, strategy_configuration=None, backtest_configuration=None):
        self.db = db
        self.harness = harness

        self.mode = None

        self._position = None
        self.order_class = Order

        # Configurable properties with defaults only below this line.

        self.volume_currency = 'BTC'

        # How long the strategy pauses between ticks.
        self.tick_sleep = 5

        # Exchanges that the strategy declares it's interested in up-front. It's
        # convenient to have these at startup sometimes.
        self.target_exchanges = []  

        if strategy_configuration:
            self.configure(strategy_configuration)

        if backtest_configuration:
            self.configure(backtest_configuration)

    def configure(self, strategy_configuration):
        """
        Initialize the strategy's configurable properties based on the configuration
        given to us by the harness, which has already been synthesized from the
        command line and .conf file.
        """
        self.init_configurable('tick_sleep', strategy_configuration)


    # def backtest_config(self, backtest_configuration):
    #     """
    #     Set backtest configuration
    #     """
    #     self.init_configurable('stake', backtest_configuration)
    #     self.init_configurable('mode', backtest_configuration)

    def set_up(self):
        """
        In this function do any setup that needs to be done on startup, before we enter
        the tick-loop, that may not be appropriate in the constructor.
        """
        pass

    def pre_tick(self):
        self._max_position = None

        # This is necessary because _position functions as an in-tick cache, so this
        # line clears that cache from last tick. Could also be done in post_tick.
        self._position = None

    def tick(self, order_book, eaten_orders):
        raise NotImplementedError

    def post_tick(self, tick_count):
        pass

    def is_complete(self):
        """
        Strategies can signal to their runners that they are "finished". This isn't
        usually relevant for continuous-trading strategies like a market maker, but is
        very useful for execution strategies, for instance.
        """
        return False

    @property
    def actor(self):
        """
        The strategy's 'actor' is how orders and trades are associated with the
        strategy in the database. As a consequence, if two strategies have the same
        actor, they have the same trade history and position.
        """
        return self.__class__.__name__.upper()

    @property
    def name(self):
        """
        The strategy's 'name' is a less formal identifier for a strategy than it's
        actor, and has nothing to do with the operation of strategies in the framework.
        Use it for things that aren't mission-critical, like to make log messages nice.
        """
        return self.__class__.__name__
   
    @property 
    def position(self):
        if self._position is not None:
            return self._position

        # Currently we just default to assuming the class's actor is it's classname,
        # but we'll improve this shortly.

        self._position = positions.fast_position(
            self.db,
            volume_currency=self.volume_currency,
            actor=self.actor,
        )

        return self._position

    def signals(self, data):
        '''
        data should be a pandas dataframe with following columns names in the same order 
        columns = [datetime, open, high, low, close, buy, sell, volume]
        where buy and sell are bool series

        easy to add order_size column and change backtrader_feed_extension to pass it 
        '''
        pass


    # ! CHECK IF BELOW CODE IS STILL RELEVANT

    def check_mode(self, mode, data_type=None):
        '''
        Return data_type depending on mode we are running  (backtest or execute)
        '''
        if mode == None:
            mode = self.mode

        if mode == 'backtest':
            data_type = 'cerebro_datafeed'
        elif mode == 'execute':
            data_type = 'pandas_dataframe'
        else :
            try:
                data_type = data_type
                self.harness.log('Missing backtest/execute parameters in config file')
            except:
                raise AttributeError('missing data_type')

        return data_type

    def  bt_to_pandas(self, btdata):
        '''
        from: https://stackoverflow.com/questions/53321608/extract-dataframe-from-pandas-datafeed-in-backtrader
        '''
        import pandas as pd
        # from matplotlib.dates import num2date
        
        get = lambda mydata: mydata.get()

        fields = {
                'open': get(btdata.open),
                'high': get(btdata.high),
                'low': get(btdata.low),
                'close': get(btdata.close),
                'volume': get(btdata.volume),
                'timestamp': get(btdata.datetime)
                }  

        time = [btdata.num2date(x) for x in get(btdata.datetime)]

        return pd.DataFrame(data=fields, index=time)

    def standardize_data(self, data, mode, data_type=None, data_path=None):
        ''' 
        We convert everything to, and return a pandas dataframe, since it
        will be the most convenient to use with trading libraries
        '''
        
        if data_type == None:
            data_type = self.check_mode(data_type, mode)

        if data_type == 'pandas_dataframe':

            df = data

            # ==> we want everything to be a pandas df not a dict 
            # o = data['open']
            # h = data['high']
            # l = data['low']
            # c = data['close']
            # hl2 = data['hl2']

        elif data_type == 'cerebro_datafeed':
            # we need to transform the cerebro datafeed into a pandas dataframe, 
            # so we can use the data with TA-Lib
            import pandas as pd

            file_extension = os.path.splitext(data_path)[1]
            
            if file_extension == '.csv':
                df = pd.read_csv(data_path,
                                    parse_dates=True,
                                    index_col=0)
                df["hl2"] = (df["high"] + df["low"]) / 2
            # elif file_extension == '.h5':
                
            #     with pd.HDFStore(datapath) as store:
            #         df = store[key]


            # ==> we want everything to be a pandas df not a dict
            # o = df["open"]
            # h = df["high"]
            # l = df["low"]
            # c = df["close"]
            # hl2 = (df["high"] + df["low"]) / 2

        else:
            raise AttributeError

        return df

                # ==> we want to return a pandas df
                # {'o': o, 
                # 'h': h,
                # 'l': l,
                # 'c': c, 
                # 'hl2': hl2}

    def pandas_generator(self, pandas_df, condition):
        '''
        generator to iterate over pandas df and send to cerebro
        '''

        for index in range(0, pandas_df.shape[0]):
            gen = pandas_df.loc[index, condition]
            yield gen 


    def go_long(self, data, mode='execute', data_type=None, data_path=None):
        '''
        backtrader_wrapper needs to be able to run this too,
        using cerebro datafeed as data

        data_type should be either pandas_dataframe, or cerebro_datafeed
        handle both differently

        need to add a mode variable so we can have go_long(mode=execute)
        and go_long(mode=backtest) at the same time and dont need to 
        rewrite both every time
        '''
        data = self.standardize_data(data, mode)
        pass

    def exit_long(self, data, mode, data_type=None, data_path=None):

        data = self.standardize_data(data, mode)
        pass

    def go_short(self, data, mode, data_type=None, data_path=None):

        data = self.standardize_data(data, mode)
        pass

    def exit_short(self, data, mode, data_type=None, data_path=None):

        data = self.standardize_data(data, mode)
        pass


