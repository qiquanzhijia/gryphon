import datetime
import json

from sqlalchemy import or_
from tornado.gen import coroutine

from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import Order


class OrderDetailHandler(BaseAPIHandler):
    @coroutine
    def get(self, order_id):
        session = self.session
        order = session.query(Order).filter_by(
            id=order_id).first()
        if not order:
            self.set_status(404)
            self.write({"error": "Order not found!"})
            return
        self.write({
            "order": order.get_info()
        })

    @coroutine
    @auth_require
    def delete(self, order_id):
        session = self.session
        order = session.query(Order).filter_by(
            id=order_id).first()
        if not order:
            self.set_status(404)
            self.write({"error": "Order not found!"})
            return
        order.deleted = 1
        order.delete_at = datetime.datetime.utcnow()
        session.flush()

    @coroutine
    @auth_require
    def post(self, order_id):
        body = json.loads(self.request.body.decode('utf-8'))
        p = body.get("order")

        session = self.session
        order = session.query(Order).filter_by(
            id=order_id).first()
        order.update_at = datetime.datetime.utcnow()
        order.state = p.get("state", order.state)
        order.amount = p.get("amount", order.amount)
        session.flush()
        session.refresh(order)
        self.write({"order": order.get_info()})


class OrderHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def get(self):
        session = self.session
        user_id = self.current_user.id
        orders = session.query(Order).filter(Order.deleted == 0)

        typ = self.get_argument("type", default="all")
        if typ == "all":
            orders = orders.filter(
                or_(Order.payee_id == user_id, Order.payer_id == user_id)
            )
        elif typ == "question":
            orders = orders.filter(
                Order.typ == "question",
                Order.payer_id == user_id
            )
        elif typ == "answer":
            orders = orders.filter(
                Order.typ == "question",
                Order.payee_id == user_id
            )
        elif typ == "offer_job":
            orders = orders.filter(
                Order.typ == "job",
                Order.payer_id == user_id
            )
        elif typ == "job":
            orders = orders.filter(
                Order.typ == "job",
                Order.payee_id == user_id
            )

        self.write({
            "orders": [
                q.get_info() for q in orders
            ]
        })

    @coroutine
    @auth_require
    def put(self):
        body = json.loads(self.request.body.decode('utf-8'))
        body = body.get("order")

        attrs = ["payer_id", "payee_id", "unit_price", "unit", "number",
                 "amount", ]
        order = Order()
        for attr in attrs:
            setattr(order, attr, body.get(attr))
        order.typ = body.get('type')
        order.typ_id = body.get('type_id')

        session = self.session
        session.add(order)
        session.flush()
        session.refresh(order)
        self.write({"order": order.get_info()})


class OrderQuestionHandler(BaseAPIHandler):
    @coroutine
    def get(self, qid):
        session = self.session
        order = session.query(Order).filter(
            Order.typ_id == qid,
            Order.typ == 'question'
            ).first()
        if not order:
            self.set_status(404)
            self.write({"error": "Order not found!"})
            return
        self.write({
            "order": order.get_info()
        })


class OrderJobHandler(BaseAPIHandler):
    @coroutine
    def get(self, jid):
        session = self.session
        order = session.query(Order).filter(
            Order.typ_id == jid,
            Order.typ == 'job'
            ).first()
        if not order:
            self.set_status(404)
            self.write({"error": "Order not found!"})
            return
        self.write({
            "order": order.get_info()
        })
