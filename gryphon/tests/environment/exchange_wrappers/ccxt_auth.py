import pyximport; pyximport.install()

from gryphon.lib.exchange.ccxt_wrapper import BitmexETHUSDExchange
from gryphon.tests.exceptional.exchange_wrappers.auth_methods import ExchangeAuthMethodsTests


class TestKrakenBTCEURAuthMethods(ExchangeAuthMethodsTests):
    def setUp(self):
        self.exchange = BitmexETHUSDExchange()