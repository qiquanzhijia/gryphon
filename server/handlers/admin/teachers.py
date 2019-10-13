import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.models import Question
from server.models import Teacher
from server.models import TeacherJob
from server.models import User


class TeachersHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        teachers = session.query(Teacher).order_by(Teacher.id.desc())
        self.render("teachers/list.html", teachers=teachers, info=None)
