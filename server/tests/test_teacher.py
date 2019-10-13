import copy
import json

from server.models import Teacher
from server.test import TestBase


class TestTeacher(TestBase):
    def count(self):
        session = self.session
        count = session.query(Teacher).count()
        return count

    def test_get(self):
        session = self.session
        t = session.query(Teacher).first()
        response = self.fetch('/api/teachers/{}'.format(t.id))
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(['create_at', 'gender', 'highest_education', 'method',
                    'idcard', 'self_evaluate', 'score',
                    'pay', 'region', 'school', 'school_subject', 'subject',
                    'time', 'id', 'username',
                    'success_order', 'good_evaluate_v']),
            sorted(json.loads(response.body)['teacher'].keys())
        )

    def test_list(self):
        count = self.count()
        response = self.fetch('/api/teachers')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['teachers']), count)

    def test_add(self):
        user = self.get_user()
        req_body = {
            "teacher": {
                "idcard": "Value",
                "method": "Value",
                "gender": "Value",
                "school": "Value",
                "school_subject": "Value",
                "highest_education": "Value",
                "pay": 12,
                "region": "Value",
                "subject": "Value",
                "time": "Value",
                "self_evaluate": "Value",
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['teacher']['id'] = 'id'
        res_body['teacher']['create_at'] = 'create_at'
        res_body['teacher']['score'] = 'score'
        response = self.fetch('/api/teachers/{}'.format(user.id),
                              method="POST",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(res_body['teacher'].keys()),
            sorted(json.loads(response.body)['teacher'].keys())
        )
