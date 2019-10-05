from delorean import Delorean

from gryphon.data_service.auditors.orderbook_auditor import OrderbookAuditor


class KrakenBTCUSDOrderbookAuditor(OrderbookAuditor):
    def __init__(self):
        super(KrakenBTCUSDOrderbookAuditor, self).__init__()
        self.exchange_name = 'KRAKEN_BTC_USD'
        product_id = 'BTC-USD'
        self.orderbook_url = 'https://api.kraken.com/0/public/Depth?pair%s' % product_id
        self.audit_time = 60

        self.acceptable_changes_threshold = 40

    def get_timestamp(self, new_orderbook):
        return Delorean().datetime
