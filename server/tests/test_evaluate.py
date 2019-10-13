import copy
import json

from server import models as m
from server.test import TestBase


class TestEvaluates(TestBase):

    def test_list(self):
        session = self.session
        user = self.get_user(3)
        count = session.query(m.UserEvaluate).filter(
            m.UserEvaluate.deleted == 0,
            m.UserEvaluate.user_id == user.id
        ).count()
        response = self.fetch('/api/evaluates/{}'.format(user.id),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['evaluates']), count)

    def test_list_limit(self):
        session = self.session
        user = self.get_user(3)
        count = session.query(m.UserEvaluate).filter(
            m.UserEvaluate.deleted == 0
        ).count()
        self.assertGreater(count, 1)
        response = self.fetch('/api/evaluates/{}?limit=1'.format(user.id),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['evaluates']), 1)

    def test_add(self):
        user = self.get_user()
        req_body = {
            "evaluate": {
                "order_id": "1",
                "user_id": "2",
                "score": "1",
                "content": "很好",
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['evaluate']['id'] = 'id'
        res_body['evaluate']['create_at'] = 'create_at'
        res_body['evaluate']['provider_id'] = 'create_at'
        response = self.fetch('/api/evaluates/{}'.format(user.id),
                              method="PUT",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(res_body['evaluate'].keys()),
            sorted(json.loads(response.body)['evaluate'].keys())
        )

    def test_show(self):
        session = self.session
        user = self.get_user(3)
        response = self.fetch('/api/evaluates/{}/{}'.format(user.id, 1),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(
            json.loads(response.body)['evaluate']['user_id'],
            user.id
        )

    def test_show_404(self):
        session = self.session
        user = self.get_user(3)
        response = self.fetch('/api/evaluates/{}/{}'.format(user.id, 100),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 404)
