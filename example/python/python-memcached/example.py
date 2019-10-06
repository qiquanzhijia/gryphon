#! /bin/python3
import decimal
import memcache
import os
from decimal import *
getcontext().prec = 6
a =str('111')
if isinstance(a, str):
    a = a.replace(",", "")
try:
    print(Decimal(a))
except decimal.InvalidOperation:
    raise ValueError(
        "amount value could not be converted to Decimal(): '{}'".format(a),
    )
print(Decimal(1) / Decimal(7.8))
print(Decimal(a))
print(decimal.Decimal(amount))
servers = os.environ.get('MEMCACHIER_SERVERS', 'localhost:11211').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')

# python-memcached only works with one server because of MemCachier's ASCII auth.
server = [servers[0]]

# TODO: currently fails with:
#   MemCached: MemCache: inet:mc1.c1.ec2.staging.memcachier.com:11211: timed out.
#   Marking dead.
mc = memcache.Client(server,
                     # defaults
                     debug=1,
                     dead_retry=30,  # seconds to wait before a retry
                     socket_timeout=3)
# MemCachier ASCII auth
# mc.set(user, passw)

mc.set("foo", "bar")
print(mc.get("foo"))
