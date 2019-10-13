import sys
import unittest

from tornado import options
from tornado.testing import AsyncHTTPTestCase

from server import app
from server import log
from server.models import User


class TestBase(AsyncHTTPTestCase):
    def get_app(self):
        options.parse_command_line([
            "",
            "--database_url=sqlite://",
        ])
        logger = log.get_logger()
        logger.disabled = True
        application = app.make_app()
        self.session = application.settings['session_factory'].make_session()
        return application

    def get_user(self, user_id=None, role="user"):
        session = self.session
        q = session.query(User).filter(User.role == role)
        if user_id:
            q = q.filter_by(id=user_id)
        user = q.first()
        return user


def main(**kwargs):

    if len(sys.argv) > 1:
        unittest.main(module=None, argv=sys.argv, **kwargs)
    else:
        unittest.main(defaultTest="all", argv=sys.argv, **kwargs)


if __name__ == '__main__':
    main()
