import copy
import json

from server import models as m
from server.test import TestBase


class TestRegions(TestBase):

    def test_list(self):
        session = self.session
        user = self.get_user()
        count = session.query(m.Region).filter(
            m.Region.deleted == 0,
            m.Region.level == 3,
            m.Region.parent_id == 2
        ).count()
        response = self.fetch('/api/regions/3/2',
                              headers={"token-id": user.token_id})
        self.assertEqual(response.code, 200)
        self.assertEqual(len(json.loads(response.body)['regions']), count)
