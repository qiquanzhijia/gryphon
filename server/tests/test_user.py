import copy
import json

from server.test import TestBase


class TestUser(TestBase):

    def test_user_get(self):
        user = self.get_user()
        response = self.fetch('/api/users/{}'.format(user.id))
        self.assertEqual(response.code, 200)
        body = {
            "user": {
                "id": user.id,
                "username": user.username,
                'pic': user.pic,
            }
        }
        self.assertDictEqual(json.loads(response.body), body)

    def test_user_update(self):
        user = self.get_user()
        new_pic = "adf"
        response = self.fetch(
            '/api/users/{}'.format(user.id),
            method="POST",
            body=json.dumps({"user": {"pic": new_pic}}),
            headers={"token-id": user.token_id}
        )
        self.assertEqual(response.code, 200)
        body = {
            "user": {
                "id": user.id,
                "username": user.username,
                'pic': new_pic,
                'role': user.role,
                'token_id': user.token_id,
            }
        }
        self.assertDictEqual(json.loads(response.body), body)

    def test_token_by_password(self):
        req_body = {
            "auth": {
                "type": "password",
                "username": "user",
                "password": "password",
            }
        }
        res_body = {
            "token": {
                'id': 'id',
                'token_id': "id",
                'role': 'user',
                'pic': "",
                'username': 'testuser'
            }
        }
        response = self.fetch('/api/token', method="POST",
                              body=json.dumps(req_body))
        self.assertEqual(response.code, 200)
        self.assertListEqual(list(res_body.keys()), list(
            json.loads(response.body).keys()))
        self.assertListEqual(sorted(res_body['token'].keys()),
                             sorted(json.loads(response.body)['token'].keys()))

    def test_token_by_token(self):
        user = self.get_user()

        req_body = {
            "auth": {
                "type": "token",
                "token_id": user.token_id,
            }
        }
        res_body = {
            "token": {
                'token_id': 'id',
                'role': 'user',
                'username': 'testuser',
                'pic': "",
                'id': 'id'
            }
        }
        response = self.fetch('/api/token', method="POST",
                              body=json.dumps(req_body))
        self.assertEqual(response.code, 200)
        self.assertListEqual(list(res_body.keys()), list(
            json.loads(response.body).keys()))
        self.assertListEqual(sorted(res_body['token'].keys()),
                             sorted(json.loads(response.body)['token'].keys()))

    def test_user_property(self):
        user = self.get_user()
        req_body = {
            "property": {
                "a": "a",
                "b": "b",
            }
        }
        res_body = copy.deepcopy(req_body)
        response = self.fetch('/api/users/{}/property'.format(user.id),
                              method="POST",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertDictEqual(req_body, res_body)

    def test_user_info(self):
        user = self.get_user()
        req_body = {
            "user_info": {
                "name": "name",
                "age": 15,
                "education": "博士",
                "gender": "男",
                "self_evaluate": "活泼可爱",
            }
        }
        response = self.fetch('/api/users/info'.format(user.id),
                              method="POST",
                              body=json.dumps(req_body),
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        res_body = json.loads(response.body)
        res_body['user_info'].pop('id')
        res_body['user_info'].pop('create_at')
        res_body['user_info'].pop('update_at')
        self.assertDictEqual(req_body, res_body)
