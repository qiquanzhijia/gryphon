import datetime
import json

from tornado.gen import coroutine

from server import log
from server.handlers.api.base import BaseAPIHandler
from server.handlers.api.base import auth_require
from server.models import AnswerKeywords
from server.models import Question
from server.utils import strutils

logger = log.get_logger()


class QuestionDetailHandler(BaseAPIHandler):
    @coroutine
    def get(self, question_id):
        session = self.session
        question = session.query(Question).filter_by(
            id=question_id).first()
        if not question:
            self.set_status(404)
            self.write({"error": "Question not found!"})
            return
        self.write({
            "question": question.get_info()
        })

    @coroutine
    @auth_require
    def delete(self, question_id):
        session = self.session
        question = session.query(Question).filter_by(
            id=question_id).first()
        if not question:
            self.set_status(404)
            self.write({"error": "Question not found!"})
            return
        question.deleted = 1
        question.delete_at = datetime.datetime.utcnow()
        session.flush()

    @coroutine
    @auth_require
    def post(self, question_id):
        body = json.loads(self.request.body.decode('utf-8'))
        body = body.get("question")

        session = self.session
        question = session.query(Question).filter_by(
            id=question_id).first()
        question.update_at = datetime.datetime.utcnow()
        atts = ['keywords', 'content', 'pay', 'state', 'attachments']
        for att in atts:
            v = body.get(att)
            if v:
                setattr(question, att, v)
        session.flush()
        session.refresh(question)
        self.write({"question": question.get_info()})


class QuestionHandler(BaseAPIHandler):

    @auth_require
    def my_question(self, questions):
        user_id = self.current_user.id
        questions = questions.filter(Question.asker_id == user_id)
        return questions


    @coroutine
    def get(self):
        session = self.session
        questions = session.query(Question)

        only_me = self.get_argument("only_me", default="false")
        only_me = strutils.bool_from_string(only_me)
        if only_me:
            questions = self.my_question(questions)

        keyword = self.get_argument("keyword", default=None)
        if keyword:
            questions = questions.filter(
                Question.keywords.like("%{}%".format(keyword))
            )

        self.write({
            "questions": [
                q.get_info() for q in questions
            ]
        })

    @coroutine
    @auth_require
    def put(self):
        body = json.loads(self.request.body.decode('utf-8'))
        logger.info(body)
        body = body.get("question")

        question = Question()
        question.asker_id = self.current_user.id

        atts = ['keywords', 'content', 'pay', 'attachments']
        for att in atts:
            v = body.get(att)
            if v:
                setattr(question, att, v)

        session = self.session
        session.add(question)
        session.flush()
        session.refresh(question)
        self.write({"question": question.get_info()})


class AnswerKeywordsHandler(BaseAPIHandler):

    @auth_require
    def get_user_keywords(self):
        session = self.session
        user_id = self.current_user.id
        keys = session.query(AnswerKeywords).filter(
            AnswerKeywords.user_id == user_id,
            AnswerKeywords.deleted == 0
        )
        return keys


    @coroutine
    def get(self):
        keys = self.get_user_keywords()

        self.write({
            "keywords": [
                k.get_info() for k in keys
            ]
        })

    @coroutine
    @auth_require
    def put(self):
        body = json.loads(self.request.body.decode('utf-8'))
        p = body.get("keyword")

        keyword = p['keyword']
        user_id = self.current_user.id

        k = AnswerKeywords(
            keyword=keyword,
            user_id=user_id
        )

        session = self.session
        session.add(k)
        session.flush()
        session.refresh(k)

        keys = self.get_user_keywords()
        self.write({
            "keywords": [
                k.get_info() for k in keys
            ]
        })


class AnswerKeywordsDetailHandler(BaseAPIHandler):

    @coroutine
    @auth_require
    def delete(self, k_id):
        session = self.session
        k = session.query(AnswerKeywords).filter_by(
            id=k_id).first()
        if not k:
            self.set_status(404)
            self.write({"error": "Keyword not found!"})
            return
        k.deleted = 1
        k.delete_at = datetime.datetime.utcnow()
        session.flush()
