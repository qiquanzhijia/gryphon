import json
import uuid

from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.models import TeacherJob


class JobsHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        jobs = session.query(TeacherJob).order_by(TeacherJob.id.desc())
        self.render("jobs/list.html", jobs=jobs)
