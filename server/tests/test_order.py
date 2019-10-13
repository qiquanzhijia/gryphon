import copy
import json

from server.models import Order
from server.test import TestBase


class TestOrder(TestBase):
    def get_count(self):
        session = self.session
        count = session.query(Order).count()
        return count

    def test_list(self):
        user = self.get_user()
        response = self.fetch('/api/orders',
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['orders']), 1)

    def test_add(self):
        user = self.get_user(2)
        req_body = {
            "order": {
                'payee_id': 3,
                'unit': '次',
                'unit_price': 1000,
                'number': 1,
                'amount': 1000,
                'type': 'question',
                'type_id': 2,
                'state': 'payed',
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['order']['id'] = 'id'
        res_body['order']['payer_id'] = user.id
        response = self.fetch('/api/orders', method="PUT",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(res_body['order'].keys()),
            sorted(json.loads(response.body)['order'].keys())
        )

    def test_get(self):
        session = self.session
        o = session.query(Order).first()
        response = self.fetch('/api/orders/{}'.format(o.id))
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(['amount', 'id', 'number', 'payee_id', 'payer_id',
                    'state', 'type', 'type_id', 'unit', 'unit_price']),
            sorted(json.loads(response.body)['order'].keys())
        )

    def test_delete(self):
        user = self.get_user()
        session = self.session
        q = session.query(Order).first()
        response = self.fetch('/api/orders/{}'.format(q.id),
                              method="DELETE",
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        count = session.query(Order).filter(Order.id == q.id).count()
        self.assertEqual(count, 1)
        count = session.query(Order).filter(
            Order.id == q.id,
            Order.deleted == 0
        ).count()
        self.assertEqual(count, 0)

    def test_update(self):
        user = self.get_user()
        session = self.session
        q = session.query(Order).first()
        req_body = {
            "order": {
                'amount': 100,
            }
        }
        response = self.fetch('/api/orders/{}'.format(q.id),
                              body=json.dumps(req_body),
                              method="POST",
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(
            json.loads(response.body)['order']["amount"],
            100
        )

    def test_get_by_job(self):
        session = self.session
        o = session.query(Order).first()
        response = self.fetch('/api/orders/job/{}'.format(2))
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(['amount', 'id', 'number', 'payee_id', 'payer_id',
                    'state', 'type', 'type_id', 'unit', 'unit_price']),
            sorted(json.loads(response.body)['order'].keys())
        )

    def test_get_by_question(self):
        session = self.session
        o = session.query(Order).first()
        response = self.fetch('/api/orders/question/{}'.format(2))
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(['amount', 'id', 'number', 'payee_id', 'payer_id',
                    'state', 'type', 'type_id', 'unit', 'unit_price']),
            sorted(json.loads(response.body)['order'].keys())
        )
