from server.handlers.api import evaluates
from server.handlers.api import regions
from server.handlers.api import schools
from server.handlers.api.msg import JobMsgHandler
from server.handlers.api.msg import JobUserMsgHandler
from server.handlers.api.msg import MsgChannelHandler
from server.handlers.api.msg import MsgHandler
from server.handlers.api.msg import QuestionMsgHandler
from server.handlers.api.msg import QuestionUserMsgHandler
from server.handlers.api.msg import UnreadMsgHandler
from server.handlers.api.msg import UserMsgHandler
from server.handlers.api.order import OrderDetailHandler
from server.handlers.api.order import OrderHandler
from server.handlers.api.order import OrderJobHandler
from server.handlers.api.order import OrderQuestionHandler
from server.handlers.api.question import AnswerKeywordsDetailHandler
from server.handlers.api.question import AnswerKeywordsHandler
from server.handlers.api.question import QuestionDetailHandler
from server.handlers.api.question import QuestionHandler
from server.handlers.api.teacher import TeacherDetailHandler
from server.handlers.api.teacher import TeacherFilterByJobHandler
from server.handlers.api.teacher import TeacherHandler
from server.handlers.api.teacher import TeacherJobDetailHandler
from server.handlers.api.teacher import TeacherJobHandler
from server.handlers.api.user import TokenHandler
from server.handlers.api.user import UserDetailHandler
from server.handlers.api.user import UserHandler
from server.handlers.api.user import UserInfoHandler
from server.handlers.api.user import UserPropertyHandler
from server.handlers.api.utils import FileHandler

api_handers = [
    (r'/api/teachers', TeacherHandler),
    (r'/api/teachers/([0-9]+)', TeacherDetailHandler),
    (r'/api/teachers/job/([0-9]+)', TeacherFilterByJobHandler),
    (r'/api/teacherjobs', TeacherJobHandler),
    (r'/api/teacherjobs/([0-9]+)', TeacherJobDetailHandler),
    (r'/api/users', UserHandler),
    (r'/api/users/([0-9]+)', UserDetailHandler),
    [r'/api/users/([0-9]+)/property', UserPropertyHandler],
    (r'/api/users/info', UserInfoHandler),
    (r'/api/token', TokenHandler),
    (r'/api/questions', QuestionHandler),
    (r'/api/questions/([0-9]+)', QuestionDetailHandler),
    (r'/api/msgs/unread', UnreadMsgHandler),
    (r'/api/msgs/read/([0-9]+)', MsgHandler),
    (r'/api/msg/([0-9]+)', UserMsgHandler),
    (r'/api/msg/question/([0-9]+)', QuestionMsgHandler),
    (r'/api/msg/question/([0-9]+)/user/([0-9]+)', QuestionUserMsgHandler),
    (r'/api/msg/job', JobMsgHandler),
    (r'/api/msg/job/([0-9]+)/user/([0-9]+)', JobUserMsgHandler),
    (r'/api/msg/channel', MsgChannelHandler),
    (r'/api/orders', OrderHandler),
    (r'/api/orders/([0-9]+)', OrderDetailHandler),
    (r'/api/orders/job/([0-9]+)', OrderJobHandler),
    (r'/api/orders/question/([0-9]+)', OrderQuestionHandler),
    (r'/api/answer_keywords', AnswerKeywordsHandler),
    (r'/api/answer_keywords/([0-9]+)', AnswerKeywordsDetailHandler),
    (r'/api/upload', FileHandler),
    (r'/api/schools', schools.SchoolsHandler),
    (r'/api/regions/([0-9]+)/(-?[0-9]+)', regions.RegionsHandler),
    (r'/api/evaluates/([0-9]+)', evaluates.EvaluatesHandler),
    (r'/api/evaluates/([0-9]+)/([0-9]+)', evaluates.EvaluateDetailHandler),
]
