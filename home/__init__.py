import os
from application import Application
from flask_sqlalchemy import SQLAlchemy
from config.local_setting import config_map

# 数据库对象
db = SQLAlchemy()
# 工厂模式


def create_app(config_name):
    app = Application(__name__, template_folder=os.getcwd() + "/home/templates/", root_path=os.getcwd())
    # 根据配置模式名字获取参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)
    return app


app = create_app("develop")