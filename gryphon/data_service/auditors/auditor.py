# -*- coding: utf-8 -*-
import os

from alchimia import TWISTED_STRATEGY
from sqlalchemy import create_engine
from twisted.internet import reactor


class Auditor(object):
    def start(self):
        raise NotImplementedError

    def audit(self):
        raise NotImplementedError

    def setup_mysql(self):

        # apparently this seems to create some problems ? 
        # similar to first time i wanted to run migrations
        # where changing create_engine etc had to be replaced by :
        # engine = engine_from_config(config.get_section(config.config_ini_section),
        # prefix='sqlalchemy.', poolclass=pool.NullPool)

        self.engine = create_engine(
            os.environ.get('DB_CRED'),
            reactor=reactor,
            strategy=TWISTED_STRATEGY,
        )

