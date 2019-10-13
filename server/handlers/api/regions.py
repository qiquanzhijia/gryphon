import json

from tornado.gen import coroutine

from server import models as m
from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require


class RegionsHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, level, parent_id):
        session = self.session
        regions = session.query(m.Region).filter(
            m.Region.deleted == 0,
            m.Region.level == level,
            m.Region.parent_id == parent_id
        )

        self.write({
            "regions": [
                r.get_info() for r in regions
            ]
        })
