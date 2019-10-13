import json
import uuid
from datetime import datetime

from tornado.gen import coroutine

from server import models as m
from server.handlers.admin.base import BaseAdminHandler


class RegionsHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        info = self.get_argument('info', None)
        regions = session.query(m.Region).filter(
            m.Region.deleted == 0,
        )
        self.render("regions/list.html", regions=regions, info=info)


class RegionDeleteHandler(BaseAdminHandler):

    @coroutine
    def post(self, *args, **kwargs):
        session = self.session
        id = self.get_argument('id', None)
        region = session.query(m.Region).filter(
            m.Region.id == id,
        ).first()
        region.deleted = 1
        region.delete_at = datetime.now()
        self.redirect(
            "/admin/regions?info=地区（{}）已经删除成功".format(region.name)
        )


class RegionAddHandler(BaseAdminHandler):

    @coroutine
    def get(self):
        session = self.session
        regions = session.query(m.Region)
        info = self.get_argument('info', None)
        err = self.get_argument('err', None)
        self.render("regions/add.html", regions=regions, info=info, err=err)

    @coroutine
    def post(self):
        session = self.session
        name = self.get_argument('name', None)
        s = None
        if not name:
            self.redirect("/admin/regions/add?err=地区名字不能为空")

        attrs = ["code", "level", "parent_id"]
        s = m.Region(name=name)
        for attr in attrs:
            setattr(s, attr, self.get_argument(attr, None))

        session.add(s)
        session.flush()
        session.refresh(s)
        self.redirect(
            "/admin/regions/add?info=地区({})已经添加成功".format(name)
        )
