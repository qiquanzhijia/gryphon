import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler, BaseHandler
from server.models import User
from server.models import UserInfo


class LoginHandler(BaseHandler):

    @coroutine
    def get(self):
        self.render("users/login.html")

    @coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username', "")
        password = self.get_argument('password', "")
        user_id = None

        session = self.session
        user = session.query(User).filter_by(username=username).first()
        if user and password == user.password and user.role == 'admin':
            user.token_id = uuid.uuid4().hex
            user_id = user.id

        if not user_id:
            self.set_status(401)
            self.write({
                "error": "User or password error!"
            })
            return

        session.flush()
        session.refresh(user)
        self.set_cookie('token-id', user.token_id)
        self.redirect("/admin")


class TokenListHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        users = session.query(User)
        token_list = [
            user.username + " : " + user.password + " : " + user.token_id
            for user in users]

        self.write("""<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<a href="/admin">index</a>
  <br>
  {}

</body>
</html>
        """.format('<br>'.join(token_list)))


class TokenHandler(BaseAdminHandler):

    @coroutine
    def delete(self, user_id):
        session = self.session
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.token_id = uuid.uuid4().hex
        self.redirect("/admin/token")


class UsersHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        users = session.query(User).order_by(User.id.desc())
        self.render("users/user_list.html", users=users)


class UserInfosHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        user_infos = session.query(UserInfo).order_by(UserInfo.id.desc())
        self.render("users/info_list.html", user_infos=user_infos)
