import os
from functools import wraps

from tornado.web import RequestHandler

from server.models import User
from server.tornado_sqlalchemy import SessionMixin


class BaseHandler(SessionMixin, RequestHandler):
    user = None
    loader = None

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), "templates")
