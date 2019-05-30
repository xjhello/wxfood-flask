# coding:utf-8
import os
from logging.handlers import RotatingFileHandler
import redis
import logging
from application import Application
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from config.local_setting import config_map

# 数据库对象
db = SQLAlchemy()
# 创建redis连接对象
redis_store = None

# 配置日志信息
# 设置日志的记录等级
# logging.basicConfig(level=logging.INFO)
# # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
# file_log_handler = RotatingFileHandler("logs/log"maxBytes=1024*1024*100backupCount=10)
# # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
# formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# # 为刚创建的日志记录器设置日志记录格式
# file_log_handler.setFormatter(formatter)
# # 为全局的日志工具对象（flask app使用的）添加日记录器
# logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    app = Application(__name__, template_folder=os.getcwd() + "/home/templates/", root_path=os.getcwd())
    # 根据配置模式名字获取参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)
    # 创建redis连接对象
    # global redis_store
    # redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    # 利用flask-session，将session数据保存到redis中
    # Session(app)
    # 为flask补充csrf防护
    # CSRFProtect(app)
    return app

app = create_app("develop")