import json
import uuid
from datetime import datetime
from datetime import timedelta

import sqlalchemy as sa
from tornado.gen import coroutine

from server.handlers.admin.base import BaseAdminHandler
from server.models import Question
from server.models import TeacherJob
from server.models import User
from server.models import UserInfo


class IndexHandler(BaseAdminHandler):

    def last_7_date_user_growth(self, kwargs):
        session = self.session
        now = datetime.now()
        dates = [(now - timedelta(days=d)).strftime('%Y-%m-%d') for d in
                 range(7, 0, -1)]
        user_growth_labels = [(now - timedelta(days=d)).strftime('%d') for d in
                              range(7, 0, -1)]

        user_data = session.query(sa.func.DATE_FORMAT(User.create_at, '%d'),
                                  sa.func.count(User.id)).filter(
            sa.func.DATE_FORMAT(User.create_at, '%Y-%m-%d').in_(dates)
        ).group_by(
            sa.func.DATE_FORMAT(User.create_at, '%d')).all()

        user_growth_data = []
        user_data = {u[0]: u[1] for u in user_data}

        for d in user_growth_labels:
            user_growth_data.append(user_data.get(d, 0))
        kwargs.update(
            user_growth_labels=user_growth_labels,
            user_growth_data=user_growth_data,
        )

    def last_7_date_question_growth(self, kwargs):
        session = self.session
        now = datetime.now()
        dates = [(now - timedelta(days=d)).strftime('%Y-%m-%d') for d in
                 range(7, 0, -1)]
        question_growth_labels = [(now - timedelta(days=d)).strftime('%d')
                                  for d in range(7, 0, -1)]

        question_data = session.query(
            sa.func.DATE_FORMAT(Question.create_at, '%d'),
            sa.func.count(Question.id)).filter(
            sa.func.DATE_FORMAT(Question.create_at, '%Y-%m-%d').in_(dates)
        ).group_by(
            sa.func.DATE_FORMAT(Question.create_at, '%d')).all()

        question_growth_data = []
        question_data = {u[0]: u[1] for u in question_data}

        for d in question_growth_labels:
            question_growth_data.append(question_data.get(d, 0))
        kwargs.update(
            question_growth_labels=question_growth_labels,
            question_growth_data=question_growth_data,
        )

    def last_7_date_job_growth(self, kwargs):
        session = self.session
        now = datetime.now()
        dates = [(now - timedelta(days=d)).strftime('%Y-%m-%d') for d in
                 range(7, 0, -1)]
        job_growth_labels = [(now - timedelta(days=d)).strftime('%d') for d in
                             range(7, 0, -1)]

        job_data = session.query(
            sa.func.DATE_FORMAT(TeacherJob.create_at, '%d'),
            sa.func.count(TeacherJob.id)).filter(
            sa.func.DATE_FORMAT(TeacherJob.create_at, '%Y-%m-%d').in_(dates)
        ).group_by(
            sa.func.DATE_FORMAT(TeacherJob.create_at, '%d')).all()

        job_growth_data = []
        job_data = {u[0]: u[1] for u in job_data}

        for d in job_growth_labels:
            job_growth_data.append(job_data.get(d, 0))
        kwargs.update(
            job_growth_labels=job_growth_labels,
            job_growth_data=job_growth_data,
        )

    def user_top_edu(self, kwargs):
        session = self.session
        info = session.query(
            UserInfo.education, sa.func.count(UserInfo.id)
        ).group_by(UserInfo.education)

        top_edu_labels = []
        top_edu_value = []

        for e, c in info:
            top_edu_labels.append(e)
            top_edu_value.append(c)

        top_edu_labels = list(map(
            lambda x: x if x else "未知",
            top_edu_labels))

        kwargs.update(
            top_edu_labels=top_edu_labels,
            top_edu_value=top_edu_value,
        )

    def user_top_gender(self, kwargs):
        session = self.session
        info = session.query(
            UserInfo.gender, sa.func.count(UserInfo.id)
        ).group_by(UserInfo.gender)

        top_gender_labels = []
        top_gender_value = []

        for e, c in info:
            top_gender_labels.append(e)
            top_gender_value.append(c)

        top_gender_labels = list(map(
            lambda x: x if x else "未知",
            top_gender_labels))

        kwargs.update(
            top_gender_labels=top_gender_labels,
            top_gender_value=top_gender_value,
        )

    def user_top_age(self, kwargs):
        session = self.session
        age_range = [
            (0, 18),
            (19, 23),
            (24, 31),
            (32, 50),
            (50, 100),
        ]

        top_age_labels = []
        top_age_value = []
        for b, e in age_range:
            top_age_labels.append("{}-{}".format(b, e))
            info = session.query(
                sa.func.count(UserInfo.id)
            ).filter(
                UserInfo.age >= b,
                UserInfo.age <= e,
            ).first()
            top_age_value.append(info[0])

        top_age_labels = list(map(
            lambda x: x if x else "未知",
            top_age_labels))

        kwargs.update(
            top_age_labels=top_age_labels,
            top_age_value=top_age_value,
        )

    @coroutine
    def get(self):
        kwargs = {}
        self.last_7_date_user_growth(kwargs)
        self.last_7_date_question_growth(kwargs)
        self.last_7_date_job_growth(kwargs)
        self.user_top_edu(kwargs)
        self.user_top_gender(kwargs)
        self.user_top_age(kwargs)

        self.render(
            "index/index.html",
            **kwargs
        )
