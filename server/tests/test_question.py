import copy
import json
import uuid

from server.models import Question
from server.test import TestBase


class TestQuestion(TestBase):
    def get_count(self):
        session = self.session
        count = session.query(Question).count()
        return count

    def test_list(self):
        count = self.get_count()
        response = self.fetch('/api/questions')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['questions']), count)

    def test_add(self):
        user = self.get_user()
        req_body = {
            "question": {
                "keywords": "keywords",
                "content": 'content',
                'attachments': "attachments",
                "pay": 'pay',
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['question']['id'] = 'id'
        res_body['question']['state'] = 'state'
        res_body['question']['asker_id'] = user.id
        response = self.fetch('/api/questions', method="PUT",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(res_body['question'].keys()),
            sorted(json.loads(response.body)['question'].keys())
        )

    def test_get(self):
        session = self.session
        q = session.query(Question).first()
        response = self.fetch('/api/questions/{}'.format(q.id))
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(['keywords', 'id', 'state', 'content', 'pay', 'asker_id',
                    'attachments']),
            sorted(json.loads(response.body)['question'].keys())
        )

    def test_delete(self):
        user = self.get_user()
        session = self.session
        q = session.query(Question).first()
        response = self.fetch('/api/questions/{}'.format(q.id),
                              method="DELETE",
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        count = session.query(Question).filter(Question.id == q.id).count()
        self.assertEqual(count, 1)
        count = session.query(Question).filter(
            Question.id == q.id,
            Question.deleted == 0
        ).count()
        self.assertEqual(count, 0)

    def test_update(self):
        user = self.get_user()
        session = self.session
        q = session.query(Question).first()
        q_info = q.get_info()
        q_info["keywords"] = "a"
        response = self.fetch('/api/questions/{}'.format(q.id),
                              body=json.dumps({
                                  "question": q_info
                              }),
                              method="POST",
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(
            json.loads(response.body)['question']["keywords"],
            "a"
        )
