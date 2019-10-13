import copy
import json

from server import models as m
from server.test import TestBase


class TestSchools(TestBase):

    def test_list(self):
        session = self.session
        user = self.get_user()
        count = session.query(m.School).filter(
            m.School.deleted == 0
        ).count()
        response = self.fetch('/api/schools',
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['schools']), count)
