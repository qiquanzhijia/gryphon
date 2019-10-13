import copy
import json

from server.models import AnswerKeywords
from server.test import TestBase


class TestAnswerkeywords(TestBase):
    def get_count(self):
        session = self.session
        count = session.query(AnswerKeywords).count()
        return count

    def test_list(self):
        user = self.get_user(2)
        count = self.get_count()
        response = self.fetch('/api/answer_keywords',
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['keywords']), count)

    def test_add(self):
        user = self.get_user()
        req_body = {
            "keyword": {
                "keyword": "keywords",
            }
        }
        res_body = copy.deepcopy(req_body)
        res_body['keyword']['id'] = 'id'
        response = self.fetch('/api/answer_keywords', method="PUT",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)

    def test_delete(self):
        user = self.get_user(2)
        session = self.session
        q = session.query(AnswerKeywords).first()
        response = self.fetch('/api/answer_keywords/{}'.format(q.id),
                              method="DELETE",
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        count = session.query(AnswerKeywords).filter(
            AnswerKeywords.id == q.id).count()
        self.assertEqual(count, 1)
        count = session.query(AnswerKeywords).filter(
            AnswerKeywords.id == q.id,
            AnswerKeywords.deleted == 0
        ).count()
        self.assertEqual(count, 0)
