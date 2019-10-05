# -*- coding: utf-8 -*-
"""
This library provides functions for creating various types of database connections.
"""


import termcolor as tc
from sqlalchemy.exc import IntegrityError
from gryphon.lib.logger import get_logger


logger = get_logger(__name__)


def get_mongo_creds():
    import os
    return os.environ['MONGO_DB']


def get_trading_db_mysql_creds():
    import os
    return os.environ['TRADING_DB_CRED']


def get_dashboard_db_mysql_creds():
    import os
    return os.environ['DASHBOARD_DB_CRED']


def get_gds_db_mysql_creds():
    import os
    return os.environ['GDS_DB_CRED']


def get_redis_creds():
    # TODO: this should throw some exception if connection info unavailable.
    import os

    env_var = os.environ.get('REDIS_URL')
    backup_env_var = os.environ.get('REDISTOGO_URL')

    return env_var if env_var else backup_env_var


def get_a_mysql_session(creds):
    import sqlalchemy
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = sqlalchemy.create_engine(
        creds,
        echo=False,
        pool_size=3,
        pool_recycle=3600,
    )

    session = scoped_session(sessionmaker(bind=engine))

    return session


def get_a_trading_db_mysql_session():
    creds = get_trading_db_mysql_creds()
    return get_a_mysql_session(creds)


def get_a_gds_db_mysql_session():
    creds = get_gds_db_mysql_creds()
    return get_a_mysql_session(creds)


def get_a_dashboard_db_mysql_session():
    creds = get_dashboard_db_mysql_creds()
    return get_a_mysql_session(creds)


def commit_mysql_session(session):
    try:
        session.commit()
    except IntegrityError: 
        session.rollback()
        logger.info(tc.colored("Integrity Error : data already exists in db", "red"))
        pass
    except Exception as e:
        session.rollback()
        raise e


def get_a_mongo_connection():
    from pymongo import MongoClient
    return MongoClient(get_mongo_creds())


def get_a_redis_connection(creds=None):
    """
    This is used for workers to get an adhoc redis connection.
    Call .connection_pool.disconnect() at the end.
    """
    if not creds:
        creds = get_redis_creds()

    import redis

    redis_client = redis.from_url(creds)

    return redis_client


def get_an_rq_connection():
    queue_conn = get_a_redis_connection()
    return queue_conn

# redis
def get_a_worker_queue():
    from rq import Queue
    queue_conn = get_an_rq_connection()
    worker_queue = Queue(connection=queue_conn)
    return worker_queue


def get_a_memcache_connection():
    import os
    # import pylibmc
    import memcache

    if (os.environ.get('MEMCACHIER_SERVERS')
            and os.environ.get('MEMCACHIER_USERNAME')
            and os.environ.get('MEMCACHIER_PASSWORD')):
        mc = memcache.Client(
            servers=os.environ.get('MEMCACHIER_SERVERS').split(','),
            # defaults
            debug=1,
            dead_retry=30,  # seconds to wait before a retry
            socket_timeout=3)
        mc.set(os.environ['MEMCACHIER_USERNAME'], os.environ['MEMCACHIER_PASSWORD'])
    else:
        # mc = pylibmc.Client(servers=['localhost:11211'])  # python-memcache
        mc = memcache.Client(servers=['localhost:11211'])

    return mc

