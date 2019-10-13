import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from server.tornado_sqlalchemy import declarative_base

DeclarativeBase = declarative_base()

AVAILABLE_ROLE = ['user', 'admin']
AVAILABLE_METHOD = ['remote', 'home']
AVAILABLE_GENDER = ['male ', 'female']
AVAILABLE_EDUCATION = ['Undergraduate', 'master', 'PhD']


def default_uuid():
    return uuid.uuid4().hex


class ObjectMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {'mysql_engine': 'InnoDB'}
    # __mapper_args__ = {'always_refresh': True}

    deleted = Column(Integer, default=0)
    hidded = Column(Integer, default=0)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, nullable=True)
    delete_at = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        for k, v in kwargs:
            setattr(self, k, v)


class User(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    pic = Column(String(255))
    role = Column(String(255))
    token_id = Column(String(255), default=default_uuid)

    jobs = relationship("TeacherJob", back_populates="provider")
    teacher = relationship("Teacher", back_populates="user")
    info = relationship("UserInfo", back_populates="user")
    questions = relationship("Question", back_populates="asker")

    def get_info(self):
        return {
            "id": self.id,
            "pic": self.pic,
            "username": self.username,
        }

    def get_token_info(self):
        info = self.get_info()
        info['token_id'] = self.token_id
        info['role'] = self.role
        return info


class UserInfo(DeclarativeBase, ObjectMixin):

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    name = Column(String(255))
    age = Column(Integer)
    education = Column(String(255))
    gender = Column(String(255))
    self_evaluate = Column(String(255))

    user = relationship("User", back_populates="info")

    def get_info(self):
        create_at = self.create_at.strftime('%Y-%m-%d %H:%M:%S') \
            if self.create_at else None
        update_at = self.update_at.strftime('%Y-%m-%d %H:%M:%S') \
            if self.update_at else None

        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "education": self.education,
            "self_evaluate": self.self_evaluate,
            "create_at": create_at,
            "update_at": update_at,
        }


class UserEvaluate(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    user_id = Column(Integer)
    score = Column(Integer)
    content = Column(String(255))
    provider_id = Column(Integer)

    def get_info(self):
        create_at = self.create_at.strftime('%Y-%m-%d %H:%M:%S') \
            if self.create_at else None

        return {
            "id": self.id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "provider_id": self.provider_id,
            "score": self.score,
            "content": self.content,
            "create_at": create_at,
        }


class UserProperty(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    property = Column(String(255))
    value = Column(String(255))


class AnswerKeywords(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    keyword = Column(String(255))

    def get_info(self):
        return {
            "id": self.id,
            "keyword": self.keyword,
        }


class TeacherJob(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    method = Column(String(255))
    gender = Column(String(255))
    school = Column(String(255))
    highest_education = Column(String(255))
    pay = Column(Integer, default=-1)
    region = Column(String(255))
    subject = Column(String(255))
    time = Column(String(255))
    provider_id = Column(Integer, ForeignKey('user.id'))

    provider = relationship("User", back_populates="jobs")

    def get_info(self):
        return {
            "id": self.id,
            "method": self.method,
            "gender": self.gender,
            "school": self.school,
            "highest_education": self.highest_education,
            "pay": self.pay,
            "region": self.region,
            "subject": self.subject,
            "time": self.time,
            "provider_id": self.provider_id,
            "create_at": self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Teacher(DeclarativeBase, ObjectMixin):

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    method = Column(String(255))
    idcard = Column(String(255))
    gender = Column(String(255))
    school = Column(String(255))
    school_subject = Column(String(255))
    highest_education = Column(String(255))
    pay = Column(Integer, default=-1)
    region = Column(String(255))
    subject = Column(String(255))
    time = Column(String(255))
    self_evaluate = Column(String(255))
    score = Column(Integer, default=-1)

    user = relationship("User", back_populates="teacher")

    def get_info(self):
        return {
            "id": self.id,
            "idcard": self.idcard,
            "method": self.method,
            "gender": self.gender,
            "school": self.school,
            "school_subject": self.school_subject,
            "highest_education": self.highest_education,
            "pay": self.pay,
            "region": self.region,
            "subject": self.subject,
            "time": self.time,
            "self_evaluate": self.self_evaluate,
            "score": self.score,
            "create_at": self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        }


question_state_create = 0
question_state_fixed = 1


class Question(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    content = Column(String(255))
    keywords = Column(String(255))
    pay = Column(Integer)
    attachments = Column(String(255))
    asker_id = Column(Integer, ForeignKey('user.id'))
    state = Column(Integer, default=0)

    asker = relationship("User", back_populates="questions")

    def get_info(self):
        return {
            'id': self.id,
            "content": self.content,
            "keywords": self.keywords,
            "attachments": self.attachments,
            "pay": self.pay,
            "asker_id": self.asker_id,
            "state": self.state
        }


AVAILABLE_ORDER_TYPE = ['question', 'job']
AVAILABLE_ORDER_STATE = ['create', 'payed', 'rejected']


class Order(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    # payer -> payee
    payer_id = Column(Integer)
    payee_id = Column(Integer)
    unit = Column(String(255))
    unit_price = Column(Integer)
    number = Column(Integer)
    amount = Column(Integer)
    typ = Column(String(255))
    typ_id = Column(Integer)
    state = Column(String(255), default='create')

    def get_info(self):
        return {
            'id': self.id,
            'payer_id': self.payer_id,
            'payee_id': self.payee_id,
            'unit': self.unit,
            'unit_price': self.unit_price,
            'number': self.number,
            'amount': self.amount,
            'type': self.typ,
            'type_id': self.typ_id,
            'state': self.state,
        }


AVAILABLE_MSG_TYPE = ['question', 'job']


class Msg(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    content = Column(String(255))
    unread = Column(Integer, default=1)
    typ = Column(String(255))
    typ_id = Column(Integer)
    
    def get_info(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'unread': self.unread,
            'type': self.typ,
            'type_id': self.typ_id
        }


class School(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    department = Column(String(255))
    location = Column(String(255))
    level = Column(String(255))
    remark = Column(String(255))

    def get_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'location': self.location,
            'level': self.level,
            'remark': self.remark,
        }


class Region(DeclarativeBase, ObjectMixin):

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255))
    parent_id = Column(Integer, default=-1)
    level = Column(Integer, default=1)

    def get_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'parent_id': self.parent_id,
            'level': self.level,
        }
