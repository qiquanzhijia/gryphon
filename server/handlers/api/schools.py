import json

from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import Order
from server.models import School


class SchoolsHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self):
        session = self.session
        schools = session.query(School).filter(School.deleted == 0)

        self.write({
            "schools": [
                s.get_info() for s in schools
            ]
        })

    @coroutine
    @auth_require
    def put(self):
        body = json.loads(self.request.body.decode('utf-8'))
        body = body.get("school")

        attrs = ["name", "department", "location", "level", "remark"]
        s = School()
        for attr in attrs:
            setattr(s, attr, body.get(attr))

        session = self.session
        session.add(s)
        session.flush()
        session.refresh(s)
        self.write({"school": s.get_info()})
