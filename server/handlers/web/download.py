
from tornado.gen import coroutine

from server.handlers.web.base import BaseHandler


class DownloadHandler(BaseHandler):

    @coroutine
    def get(self):
        self.render(
            "download/download.html",
        )
