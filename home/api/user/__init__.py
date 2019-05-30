# coding:utf-8
from flask import Blueprint

# 创建蓝图对象
route_user = Blueprint('user_page', __name__)

# 导入视图函数
from . import User