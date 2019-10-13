import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.models import Question
from server.models import User


class QuestionsHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        questions = session.query(Question).order_by(Question.id.desc())
        self.render("questions/list.html", questions=questions)
