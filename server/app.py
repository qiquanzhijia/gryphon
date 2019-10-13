# coding=utf-8
import os

from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.web import Application
from tornado.web import StaticFileHandler

from server import log
from server.conf import static_path
from server.conf import upload_path
from server.conf import web_app_path
from server.handlers.admin import admin_handers
from server.handlers.api import api_handers
from server.handlers.web import web_handers
from server.init import insert_init_data
from server.models import DeclarativeBase
from server.tornado_sqlalchemy import make_session_factory


def init():
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)


def make_app():
    session_factory = make_session_factory(options.database_url)
    DeclarativeBase.metadata.create_all(session_factory.engine)
    insert_init_data(session_factory)

    handlers = [
        (r"/static/(.*)", StaticFileHandler, {"path": static_path}),
        (r"/uploads/(.*)", StaticFileHandler, {"path": upload_path}),
        (r"/app/(.*)", StaticFileHandler, {"path": web_app_path}),
        (r"/(config\.xml)", StaticFileHandler, {"path": web_app_path}),
    ]
    handlers.extend(web_handers)
    handlers.extend(api_handers)
    handlers.extend(admin_handers)
    return Application(
        handlers,
        session_factory=session_factory,
        static_path=static_path,
        cookie_secret="61oETz23rEGaYdghF1hgfhfhfg",
        debug=True,
    )


def main():
    options.parse_config_file(".env", final=False)
    # if true, If ``final`` is ``False``, parse callbacks will not be run.
    # This is useful for applications that wish to combine configurations
    # from multiple sources.
    options.parse_command_line()
    log.setup()
    init()

    make_app().listen(7777)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
