import json

from sqlalchemy import and_
from sqlalchemy import or_

from server.models import Msg
from server.models import Question
from server.test import TestBase


class TestMsg(TestBase):

    def get_unread_count(self, receiver_id, sender_id=None):
        session = self.session
        msgs = session.query(Msg).filter(
            Msg.receiver_id == receiver_id,
            Msg.unread == 1
        )
        if sender_id:
            msgs = msgs.filter(Msg.sender_id == sender_id)
        count = msgs.count()
        return count

    def get_msg_count(self, user1_id, user2_id):
        session = self.session
        count = session.query(Msg).filter(or_(
            and_(Msg.receiver_id == user1_id, Msg.sender_id == user2_id),
            and_(Msg.receiver_id == user2_id, Msg.sender_id == user1_id)
        )).count()
        return count

    def test_unauth(self):
        response = self.fetch('/api/msgs/unread')
        self.assertEqual(response.code, 401)

    def test_list_unread(self):
        user = self.get_user()
        count = self.get_unread_count(user.id)
        response = self.fetch('/api/msgs/unread',
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertGreater(count, 0)
        self.assertEqual(len(json.loads(response.body)['msgs']), count)

    def test_msg_with_user(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_msg_count(user1.id, user2.id)
        response = self.fetch('/api/msg/{}'.format(user2.id),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        self.assertGreater(count, 0)
        self.assertEqual(len(json.loads(response.body)['msgs']), count)

    def test_msg_read(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_unread_count(user1.id, user2.id)
        self.assertGreater(count, 0)
        response = self.fetch('/api/msg/{}'.format(user2.id),
                              method="POST",
                              body=json.dumps({}),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        count = self.get_unread_count(user1.id, user2.id)
        self.assertEqual(count, 0)

    def test_msg_put(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_msg_count(user1.id, user2.id)
        msg_info = {
            "sender_id": user1.id,
            "receiver_id": user2.id,
            "content": "是",
            "type": "question",
            "type_id": 1,
        }
        response = self.fetch('/api/msg/{}'.format(user2.id),
                              method="PUT",
                              body=json.dumps({
                                  "msg": msg_info
                              }),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        c2 = self.get_msg_count(user1.id, user2.id)
        self.assertEqual(count + 1, c2)

    def test_question_msg(self):
        session = self.session
        user1 = self.get_user(2)
        q = session.query(Question).filter(Question.id == 2).first()
        response = self.fetch('/api/msg/question/{}'.format(q.id),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        msgs = json.loads(response.body)['msgs']
        self.assertEqual(len(msgs), 2)
        self.assertListEqual(
            [3, 2],
            [m['id'] for m in msgs]
        )

    def test_question_msg_put(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_msg_count(user1.id, user2.id)
        msg_info = {
            "content": "是",
        }
        response = self.fetch(
            '/api/msg/question/{}/user/{}'.format(1, user2.id),
            method="PUT",
            body=json.dumps({
                "msg": msg_info
            }),
            headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        c2 = self.get_msg_count(user1.id, user2.id)
        self.assertEqual(count + 1, c2)

    def test_job_msg(self):
        user1 = self.get_user(3)
        response = self.fetch('/api/msg/job'.format(1),
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        msgs = json.loads(response.body)['msgs']
        self.assertEqual(len(msgs), 2)
        self.assertListEqual(
            [9, 6],
            [m['id'] for m in msgs]
        )

    def test_job_msg_put(self):
        user1 = self.get_user(2)
        user2 = self.get_user(3)
        count = self.get_msg_count(user1.id, user2.id)
        msg_info = {
            "content": "是",
        }
        response = self.fetch(
            '/api/msg/job/{}/user/{}'.format(1, user2.id),
            method="PUT",
            body=json.dumps({
                "msg": msg_info
            }),
            headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        c2 = self.get_msg_count(user1.id, user2.id)
        self.assertEqual(count + 1, c2)

    def test_channel_msg(self):
        user1 = self.get_user(3)
        response = self.fetch('/api/msg/channel',
                              headers={"token-id": user1.token_id})
        self.assertEqual(response.code, 200)
        msgs = json.loads(response.body)['msgs']
        self.assertEqual(len(msgs), 3)
        self.assertListEqual(
            [9, 6, 4],
            [m['id'] for m in msgs]
        )
