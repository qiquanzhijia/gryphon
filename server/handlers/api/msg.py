import json
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_
from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import Msg
from server.models import TeacherJob


class UnreadMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self):
        session = self.session
        msgs = session.query(Msg).filter(
            Msg.receiver_id == self.current_user.id,
            Msg.unread == 1,
            Msg.deleted == 0
        )
        self.write({
            "msgs": [
                m.get_info() for m in msgs
            ]
        })


class MsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def post(self, msg_id):
        with self.make_session() as session:
            msg = session.query(Msg).filter(
                Msg.id == msg_id
            ).first()

            if not msg:
                self.set_status(404)
                self.write({"error": "Not found!"})
                return

            msg.unread = 0
            msg.update_at = datetime.now()

            self.write({
                "msg": [
                    msg.get_info()
                ]
            })


class MsgChannelHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self):
        session = self.session

        msgs = session.query(Msg).filter(
            Msg.id.in_(
                session.query(func.max(Msg.id)).filter(
                    or_(
                        Msg.sender_id == self.current_user.id,
                        Msg.receiver_id == self.current_user.id,
                    ),
                    Msg.deleted == 0
                ).group_by(Msg.typ, Msg.typ_id)
            )
        ).group_by(Msg.typ, Msg.typ_id).order_by(
            Msg.id.desc()
        )

        self.write({
            "msgs": [
                m.get_info() for m in msgs
            ]
        })


class QuestionMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, qid):
        session = self.session
        user_id = self.current_user.id

        msgs = session.query(Msg).filter(
            Msg.id.in_(
                session.query(func.max(Msg.id)).filter(
                    Msg.typ == "question",
                    Msg.typ_id == qid,
                    Msg.sender_id != user_id
                ).group_by(Msg.sender_id)
            )
        ).order_by(Msg.id.desc())

        self.write({
            "msgs": [
                m.get_info() for m in msgs
            ]
        })


class QuestionUserMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, qid, uid):
        session = self.session
        msgs = session.query(Msg).filter(
            Msg.typ == "question",
            Msg.typ_id == qid,
            or_(
                and_(
                    Msg.receiver_id == uid,
                    Msg.sender_id == self.current_user.id
                ),
                and_(
                    Msg.receiver_id == self.current_user.id,
                    Msg.sender_id == uid
                )
            )
        )
        self.write({
            "msgs": [
                m.get_info() for m in msgs
            ]
        })

    @coroutine
    @auth_require
    def put(self, qid, uid):
        body = json.loads(self.request.body.decode('utf-8'))
        msg = body.get("msg")

        content = msg['content']
        typ = "question"
        typ_id = qid

        with self.make_session() as session:
            msg = Msg(sender_id=self.current_user.id, receiver_id=uid,
                      content=content, typ=typ, typ_id=typ_id, unread=1)
            session.add(msg)
            session.flush()
            session.refresh(msg)
            self.write({"msg": msg.get_info()})


class JobMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self):
        session = self.session
        user_id = self.current_user.id

        msgs = session.query(Msg).filter(
            Msg.id.in_(
                session.query(func.max(Msg.id)).join(
            TeacherJob,
            TeacherJob.id == Msg.typ_id,
        ).filter(
            Msg.typ == "job",
            Msg.receiver_id == user_id,
            Msg.sender_id != user_id,
            TeacherJob.provider_id != user_id
        ).group_by(Msg.sender_id)
            )
        ).order_by(Msg.id.desc())

        self.write({
            "msgs": [
                m.get_info() for m in msgs
            ]
        })


class JobUserMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, jid, uid):
        session = self.session
        msgs = session.query(Msg).filter(
            Msg.typ == "job",
            Msg.typ_id == jid,
            or_(
                and_(
                    Msg.receiver_id == uid,
                    Msg.sender_id == self.current_user.id
                ),
                and_(
                    Msg.receiver_id == self.current_user.id,
                    Msg.sender_id == uid
                )
            )
        )
        self.write({
            "msgs": [
                m.get_info() for m in msgs
            ]
        })

    @coroutine
    @auth_require
    def put(self, jid, uid):
        body = json.loads(self.request.body.decode('utf-8'))
        msg = body.get("msg")

        content = msg['content']
        typ = "job"
        typ_id = jid

        with self.make_session() as session:
            msg = Msg(sender_id=self.current_user.id, receiver_id=uid,
                      content=content, typ=typ, typ_id=typ_id, unread=1)
            session.add(msg)
            session.flush()
            session.refresh(msg)
            self.write({"msg": msg.get_info()})


class UserMsgHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, user_id=None):
        session = self.session
        msgs = session.query(Msg).filter(or_(
            and_(
                Msg.receiver_id == user_id,
                Msg.sender_id == self.current_user.id
            ),
            and_(
                Msg.receiver_id == self.current_user.id,
                Msg.sender_id == user_id
            )
        ))

        self.write({
            "msgs": [
                m.get_info() for m in msgs
            ]
        })

    @coroutine
    @auth_require
    def put(self, receiver_id):
        body = json.loads(self.request.body.decode('utf-8'))
        msg = body.get("msg")

        content = msg['content']
        typ = msg['type']
        typ_id = msg['type_id']

        with self.make_session() as session:
            msg = Msg(sender_id=self.current_user.id, receiver_id=receiver_id,
                      content=content, typ=typ, typ_id=typ_id)
            session.add(msg)
            session.flush()
            session.refresh(msg)
            self.write({"msg": msg.get_info()})

    @coroutine
    @auth_require
    def post(self, sender_id):
        with self.make_session() as session:
            msgs = session.query(Msg).filter(
                Msg.receiver_id == self.current_user.id,
                Msg.sender_id == sender_id
            )
            for msg in msgs:
                msg.unread = 0
            return {
                "success": "All massages marked read."
            }
