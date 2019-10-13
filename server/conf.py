# coding=utf-8
import os

from tornado.options import define

define("database_url",
       default="mysql+pymysql://root:@localhost/t_sa?charset=utf8",
       help="Main user DB")

server_path = os.path.dirname(__file__)
root_path = os.path.dirname(server_path)
static_path = os.path.join(server_path, "static")
web_app_path = os.path.join(root_path, "app")
upload_path = os.path.join(root_path, "uploads")
