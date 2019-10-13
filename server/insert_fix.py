import random
from datetime import datetime
from datetime import timedelta

from tornado.options import options

from server import conf
from server import models as m
from server.tornado_sqlalchemy import make_session_factory


def insert_fix(session):

    edu = {}
    for i in range(1, 11):
        edu[i] = '本科'
    for i in range(11, 13):
        edu[i] = '硕士'
    edu[13] = '博士'
    for i in range(13, 20):
        edu[i] = '其他'

    eva = [
        '本人性格开朗，为人细心，做事一丝不苟，能吃苦耐劳，工作脚踏实地。',
        '本人性格开朗，为人细心',
        '做事一丝不苟，能吃苦耐劳',
        '工作脚踏实地，有较强的责任心',
        '有责任心、人品好、思想端正；',
        '极强的沟通能力与谈判能力',
        '能熟练运用Windows Office Word、Excel、XXX等应用软件',
        '具备良好的责任意识',
        '有较强的责任心，具有团队合作精神',
        '思维活跃。',
        '本人热爱学习，工作态度严谨认真，责任心强',
        '本人性格活泼开朗，与人相处和睦融洽，有较强的沟通能力。',
        '拥有较强的组织能力和协调能力，并具有良好的身体素质。',
        '本人性格开朗、稳重、有活力，待人热情、真诚；工作认真负责，积极主动，能吃苦耐劳，用于承受压力，勇于创新；',
        '善与人交流，人际关系良好，待人诚恳；',
        '工作认真负责，具有吃苦耐劳、艰苦奋斗的精神；',
        '沉着冷静，理智稳重，适应能力强',
        '热情开朗，待人友好，为人诚实谦虚',
        '品学兼优，连续三年获得学院奖学金。',
        '吃苦耐劳、勇于迎接新挑战。',
        '活泼开朗、乐观向上、兴趣广泛、适应力强',
    ]

    users = session.query(m.User, m.UserInfo).outerjoin(
        m.UserInfo, m.User.id == m.UserInfo.id
    ).all()

    for user, info in users:
        if random.randint(1, 10) > 8:
            continue
        if not info:
            i = m.UserInfo(
                id=user.id,
                name=user.username,
                gender='男' if random.randint(1, 2) > 1 else '女',
                education=edu[random.randint(1, 19)],
                self_evaluate=eva[random.randint(1, len(eva)-1)]
            )
            session.add(i)


def fix_age(session):
    age = {}
    for i in range(1, 11):
        age[i] = lambda: random.randint(18, 22)
    for i in range(11, 15):
        age[i] = lambda: random.randint(23, 30)
    for i in range(15, 17):
        age[i] = lambda: random.randint(31, 50)

    infos = session.query(m.UserInfo)
    for i in infos:
        if not i.age and i.name:
            i.age = age[random.randint(1, 16)]()


def fix_user_create_at(session):
    users = session.query(m.User).order_by(m.User.id.desc())
    count = 0
    day = -1
    minutes = 0
    for u in users:
        if not count:
            count = random.randint(15, 35)
            minutes = 0
            day = day + 1
        t = datetime.now()
        t = t - timedelta(days=day, minutes=minutes,
                          seconds=random.randint(10, 50))
        minutes = minutes + random.randint(12, 40)
        count = count - 1
        u.create_at = t


def fix_queston_create_at(session):
    questions = session.query(m.Question).order_by(m.Question.id.desc())
    count = 0
    day = -1
    minutes = 0
    for q in questions:
        if not count:
            count = random.randint(12, 25)
            minutes = 0
            day = day + 1
        t = datetime.now()
        t = t - timedelta(days=day, minutes=minutes,
                          seconds=random.randint(10, 50))
        minutes = minutes + random.randint(12, 40)
        count = count - 1
        q.create_at = t


def fix_job_create_at(session):
    jobs = session.query(m.TeacherJob).order_by(m.TeacherJob.id.desc())
    count = 0
    day = -1
    minutes = 0
    for j in jobs:
        if not count:
            count = random.randint(5, 15)
            minutes = 0
            day = day + 1
        t = datetime.now()
        t = t - timedelta(days=day, minutes=minutes,
                          seconds=random.randint(10, 50))
        minutes = minutes + random.randint(12, 40)
        count = count - 1
        j.create_at = t


def fix_user_id(session):
    uids = []
    users = session.query(m.User).filter(
        m.User.role == 'user',
    )

    for user in users:
        uids.append(user.id)
    u_len = len(uids) - 1

    jobs = session.query(m.TeacherJob)
    for j in jobs:
        j.provider_id = uids[random.randint(0, u_len)]

    qs = session.query(m.Question)
    for q in qs:
        q.asker_id = uids[random.randint(0, u_len)]


def fix_question_state(session):
    qs = session.query(m.Question)
    for q in qs:
        if random.randint(1, 5) != 1:
            continue
        q.state = 1


def main():
    options.parse_config_file("server.ini", final=False)
    options.parse_command_line()
    session_factory = make_session_factory(options.database_url)
    m.DeclarativeBase.metadata.create_all(session_factory.engine)
    session = session_factory.make_session()
    fix_user_create_at(session)
    fix_queston_create_at(session)
    fix_job_create_at(session)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
