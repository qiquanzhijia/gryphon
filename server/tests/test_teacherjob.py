import copy
import json
import uuid

from server.models import TeacherJob
from server.test import TestBase


class TestJob(TestBase):
    def count(self):
        session = self.session
        count = session.query(TeacherJob).count()
        return count

    def test_get(self):
        session = self.session
        j = session.query(TeacherJob).first()
        response = self.fetch('/api/teacherjobs/{}'.format(j.id))
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(['create_at', 'gender', 'highest_education', 'id', 'method',
                    'pay', 'region', 'school', 'subject', 'time',
                    'provider_id']),
            sorted(json.loads(response.body)['teacherjob'].keys()))

    def test_list(self):
        count = self.count()
        response = self.fetch('/api/teacherjobs')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['teacherjobs']), count)

    def test_add(self):
        user = self.get_user()
        req_body = {
            "teacherjob": {
                'gender': "a",
                'highest_education': "ed",
                'method': "",
                'pay': "",
                'region': "",
                'school': "",
                'subject': "",
                'time': ""
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['teacherjob']['id'] = 'id'
        res_body['teacherjob']['create_at'] = 'create_at'
        res_body['teacherjob']['provider_id'] = 'provider_id'
        response = self.fetch('/api/teacherjobs',
                              method="PUT",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertListEqual(
            sorted(res_body['teacherjob'].keys()),
            sorted(json.loads(response.body)['teacherjob'].keys()))

    def test_list_by_job(self):
        response = self.fetch('/api/teachers/job/3')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['teachers']), 1)
