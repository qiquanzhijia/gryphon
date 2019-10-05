import pyximport; pyximport.install()

from gryphon.lib.exchange.ccxt_wrapper import BitmexETHUSDExchange
from gryphon.tests.exceptional.exchange_wrappers.live_orders import LiveOrdersTest


class TestBitmexBTCUSDLiveOrders(LiveOrdersTest):
    def __init__(self):
        self.order1_price_amount = '0.1'
        self.order2_price_amount = '0.2'
        self.sleep_time = 3  

    def setUp(self):
        self.exchange = BitmexETHUSDExchange()