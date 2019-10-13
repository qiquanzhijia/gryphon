import pyximport; pyximport.install()
# cython: language_level=3
import logging
import os
import unittest
import sure
import mock
from gryphon.lib.exchange.exchange_api_wrapper import ExchangeAPIWrapper
logger = logging.getLogger(__name__)


class ExchangePublicMethodsTests(ExchangeAPIWrapper):
    def __init__(self, session=None, configuration=None):
        super(ExchangePublicMethodsTests, self).__init__(session, configuration)

    def test_orderbook(self):
        book = self.exchange.get_orderbook()

        assert len(book['bids']) > 10
        assert len(book['asks']) > 10

    def test_ticker(self):
        ticker = self.exchange.get_ticker()

        assert all([key in ticker for key in ('high', 'low', 'last', 'volume')])

