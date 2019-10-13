import json
import uuid
from datetime import datetime

from tornado.gen import coroutine

from server import models as m
from server.handlers.admin.base import BaseAdminHandler


class SchoolsHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        info = self.get_argument('info', None)
        schools = session.query(m.School).filter(
            m.School.deleted == 0,
        )
        self.render("schools/list.html", schools=schools, info=info)


class SchoolDeleteHandler(BaseAdminHandler):

    @coroutine
    def post(self, *args, **kwargs):
        session = self.session
        id = self.get_argument('id', None)
        school = session.query(m.School).filter(
            m.School.id == id,
        ).first()
        school.deleted = 1
        school.delete_at = datetime.now()
        self.redirect(
            "/admin/schools?info=学校（{}）已经删除成功".format(school.name)
        )


class SchoolAddHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        schools = session.query(m.School)
        info = self.get_argument('info', None)
        err = self.get_argument('err', None)
        self.render("schools/add.html", schools=schools, info=info, err=err)

    @coroutine
    def post(self):
        session = self.session
        name = self.get_argument('name', None)
        s = None
        if name:
            s = session.query(m.School).filter(
                m.School.name == name
            ).first()
            if s and s.deleted == 0:
                self.redirect("/admin/schools/add?err=学校已经存在")
        else:
            self.redirect("/admin/schools/add?err=学校名字不能为空")

        attrs = ["department", "location", "level", "remark"]
        if not s:
            s = m.School(name=name)
        else:
            s.deleted = 0
        for attr in attrs:
            setattr(s, attr, self.get_argument(attr, None))

        session.add(s)
        session.flush()
        session.refresh(s)
        self.redirect(
            "/admin/schools/add?info=学校({})已经添加成功".format(name)
        )
