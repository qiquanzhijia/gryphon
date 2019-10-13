import json

from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import UserEvaluate


class EvaluatesHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, user_id):
        session = self.session
        limit = self.get_argument("limit", default=None)
        evaluates = session.query(UserEvaluate).filter(
            UserEvaluate.deleted == 0,
            UserEvaluate.user_id == user_id
        )
        if limit:
            evaluates = evaluates.limit(int(limit))

        self.write({
            "evaluates": [
                s.get_info() for s in evaluates
            ]
        })

    @coroutine
    @auth_require
    def put(self, user_id):
        body = json.loads(self.request.body.decode('utf-8'))
        body = body.get("evaluate")

        attrs = ["order_id", "score", "content"]
        s = UserEvaluate()
        s.user_id = user_id
        s.provider_id = self.current_user.id
        for attr in attrs:
            setattr(s, attr, body.get(attr))

        session = self.session
        session.add(s)
        session.flush()
        session.refresh(s)
        self.write({"evaluate": s.get_info()})


class EvaluateDetailHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self, user_id, order_id):
        session = self.session
        evaluate = session.query(UserEvaluate).filter(
            UserEvaluate.deleted == 0,
            UserEvaluate.user_id == user_id,
            UserEvaluate.order_id == order_id
        ).first()

        if not evaluate:
            self.set_status(404)
            self.write({"error": "Not found!"})
            return

        self.write({
            "evaluate": evaluate.get_info()
        })
