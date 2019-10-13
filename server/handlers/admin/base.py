import os

from tornado.web import RequestHandler

from server.models import User
from server.tornado_sqlalchemy import SessionMixin


class BaseHandler(SessionMixin, RequestHandler):

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), "templates")


class BaseAdminHandler(BaseHandler):

    def get_current_user(self):
        token_id = self.get_cookie('token-id')
        if not token_id:
            return None
        user = self.session.query(User).filter_by(token_id=token_id).first()
        if not user or user.role != 'admin':
            return None
        return user

    def prepare(self):
        user = self.current_user
        if not user or user.role != 'admin':
            self.redirect("/admin/login")
