import json

from autobahn.twisted.websocket import connectWS, WebSocketClientFactory
from decimal import Decimal
from twisted.internet import defer, ssl, reactor
from twisted.internet import protocol
from txredis.client import RedisClient

import gryphon.data_service.consts as consts
import gryphon.data_service.util as util
from gryphon.data_service.websocket_client import EmeraldWebSocketClientProtocol
from gryphon.data_service.pollers.orderbook.websocket.websocket_orderbook_poller import WebsocketOrderbookPoller
from gryphon.lib.logger import get_logger

from gryphon.data_service.util import debug
import termcolor as tc

logger = get_logger(__name__)


class KrakenBTCUSDOrderbookWebsocket(EmeraldWebSocketClientProtocol, WebsocketOrderbookPoller):
    def __init__(self):
        self.exchange_name = u'KRAKEN_BTC_USD'
        self.ping_interval = 5
        self.redis = None

    def connect_to_websocket(self):
        logger.info('Connecting to websocket')

        factory = WebSocketClientFactory('wss://ws.kraken.com')

        factory.protocol = type(self)

        if factory.isSecure:
            context_factor = ssl.ClientContextFactory()
        else:
            context_factor = None

        connectWS(factory, context_factor)

    def subscribe_to_websocket(self):
        # https://www.kraken.com/features/websocket-api#connectionDetails

        logger.info('Subscribing to websocket')

        data = {
            'event': 'subscribe',
            'subscription': {'name':'book', 'depth':1000 },    # dict with keys: name, interval, depth
            'pair': ['XBT/USD'],                               # list
            }


        self.sendMessage(json.dumps(data))

    # WEBSOCKET CLIENT FUNCTIONS

    @defer.inlineCallbacks
    def onOpen(self):

        logger.info('Connected to websocket')

        reactor.callLater(self.ping_interval, self.keepalive)   # copied from coinbase websocket
        
        # self.redis = yield util.setup_redis() # testing out another way to get redis
        # logger.info('redis -- type : {0} -- {1}'.format(self.redis, type(self.redis)))

        clientCreator = protocol.ClientCreator(reactor, RedisClient)
        self.redis = yield clientCreator.connectTCP('localhost', 6379)

        binding_key = '%s.orderbook.tinker' % self.exchange_name.lower()
        self.producer = yield util.setup_producer(consts.ORDERBOOK_QUEUE, binding_key)

        # Reset everything.
        self.orderbook = {'bids': None, 'asks': None}
        self.bids_dict = {}
        self.asks_dict = {}
        self.channel_id = None
        self.have_gotten_base_orderbook = False
        self.last_amqp_push = 0

        yield self.redis.set(self.orderbook_key, None)

        self.subscribe_to_websocket()

    @defer.inlineCallbacks
    def onMessage(self, payload, isBinary):
        should_continue = yield self.check_should_continue()

        if not should_continue:
            yield self.redis.set(self.orderbook_key, None)
            return

        payload = json.loads(payload, parse_float=Decimal)

        # Initial subscription confirmation.
        if 'status' in payload and payload['status'] == 'subscribed':
            self.channel_id = payload['channelID']
            return

        # if not 'status' in payload we know that it is the book stream 
        channel_id = payload[0]

        assert(channel_id == self.channel_id)

        # The first message after subscribing is always the base orderbook.
        if not self.have_gotten_base_orderbook:
            base_orderbook = payload[1]
            self.set_base_orderbook(base_orderbook)
            self.have_gotten_base_orderbook = True
            self.publish_orderbook()

            return

        # If we are not in one of the two initial special cases
        # then we have an orderbook change event of the format:
        # [channel_id, price, num_orders, volume_diff]
        change = payload[1:]

        self.apply_change_to_orderbook(change)
        self.publish_orderbook()

    def set_base_orderbook(self, base_orderbook):

        for order in base_orderbook['bs']:
            self.bids_dict[order[0]] = order[1]

        for order in base_orderbook['as']:
            self.asks_dict[order[0]] = order[1]

    def apply_change_to_orderbook(self, change):
        '''
        snapshot[1] = dict {'as':[price, vol, timestamp], 'bs':[p, vol, ts]} with 'as','bs' = asks,bids
        update[1] same as snapshot except 'as','bs' becomes 'a','b'
        '''
        
        for order in change['b']:
            self.bids_dict[order[0]] = order[1]

        for order in change['a']:
            self.asks_dict[order[0]] = order[1]

    def get_orderbook_to_publish(self):
        # We store the orderbook internally as a bid and ask dict, so we convert it here
        # to sorted lists of [price, volume] orders.
        bids = []
        asks = []

        for price, volume in sorted(self.bids_dict.items(), reverse=True):
            if volume > 0:
                bids.append([str(price), str(volume), ''])

        for price, volume in sorted(self.asks_dict.items()):
            if volume > 0:
                asks.append([str(price), str(volume), ''])

        orderbook = {}
        orderbook['bids'] = bids
        orderbook['asks'] = asks

        return orderbook

    def print_orderbook(self):
        """Print current orderbook in format similar to Bitfinex's homepage orderbook"""
        bids = self.orderbook['bids']
        asks = self.orderbook['asks']

        if not bids or not asks:
            return

        # Pushes orderbook to bottom of terminal for a live-updating effect.
        logger.info("\n" * 100)
        logger.info('{:=^78}'.format(' ORDER BOOK '))
        logger.info('{: ^39}{: ^39}'.format('BIDS', 'ASKS'))

        titles = "{:^7} | {:^12} | {:^12} ||| {:^12} | {:^12} | {:^7}".format(
            'Price',
            'Amount',
            'Cumulative',
            'Cumulative',
            'Amount',
            'Price',
        )

        logger.info(titles)

        bid_sum = 0
        ask_sum = 0

        while bids and asks:
            bid = bids.pop(0)
            ask = asks.pop(0)

            bid_sum += bid[1]
            ask_sum += ask[1]

            line = "{:^7.1f} | {:^12.1f} | {:^12.1f} ||| {:^12.1f} | {:^12.1f} | {:^7.1f}".format(
                bid[0],
                bid[1],
                bid_sum,
                ask_sum,
                ask[1],
                ask[0]
            )

            logger.info(line)


    # @defer.inlineCallbacks
    # def check_should_continue(self):
    #     should_continue_key = '%s_orderbook_should_continue' % self.exchange_name.lower()
    #     logger.info(tc.colored(dir(self.redis), 'red'))
    #     should_continue = yield self.redis.get(should_continue_key)
    #     if not should_continue:
    #         raise KeyError('Expecting %s key in redis.' % should_continue_key)
    #     should_continue = bool(int(should_continue))

    #     if not should_continue:
    #         logger.debug('%s Orderbook Poller respecting Auditor hard failure.' % self.exchange_name)

    #     defer.returnValue(should_continue)



## ! COINBASE WEBSOCKET SEEMS MORE EXHAUSTIVE

    def keepalive(self):
        """
        Sends a keepalive ping to the Coinbase Websocket every 5 seconds. 5s is chosen
        so that we avoid the 10s "Cached orderbook too old" errors on gryphon-fury.
        Without any ping, the connection gets closed after 60 seconds of no messages.
        """
        logger.debug('Ping')
        self.sendPing('keepalive')

        reactor.callLater(self.ping_interval, self.keepalive)

    def onPong(self, payload):
        """
        Catch the pong back from Coinbase, and know that we are still successfully
        connected.
        """
        # We had one day where the Coinbase fundamental value did not change all day.
        # We think this may have been caused by them Ponging our Pings, but not
        # actually sending any data. Since Coinbase is so critical to our system, we
        # are only re-publishing orderbooks when there is an actual update (not just a
        # pong).
        logger.debug("Pong")