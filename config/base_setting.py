# # -*- coding: utf-8 -*-
# SERVER_PORT = 8999
# DEBUG = False
# SQLALCHEMY_ECHO = True  # 将所有SQL语句打印出来
#
# SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/food_db?charset=utf8mb4'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ENCODING = "utf8mb4"  # 编码
#
# AUTH_COOKIE_NAME = "mooc_food"  # cookie名称
#
# # 过滤url
# IGNORE_URLS = [
#     "^/user/login",
#     # "^/api",
#
# ]
# # 完全不用判断的url
# IGNORE_CHECK_LOGIN_URLS = [
#     "^/static",
#     "^/favicon.ico"
# ]
#
# # api访问拦截器忽略
# API_IGNORE_URLS = [
#     "^/api",
# ]
#
# MINA_APP = {  # 小程序开发者参数
#     'appid': 'wx3531ec6cb6dce0ef',
#     'appkey': 'cf5f6f28d7571d63b4f04bd1fff4765a',
# }
#
# PAGE_SIZE = 50  # 每页多少条
# PAGE_DISPLAY = 10  # 显示的总页数
#
# STATUS_MAPPING = {  # 账户状态
#     "1": "正常",
#     "0": "已删除"
# }
#
# # 上传的图片设置
# UPLOAD = {
#     'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
#     'prefix_path': '/web/static/upload/',
#     'prefix_url': '/static/upload/'
# }
#
# # 域名
# APP = {
#     'domain': 'http://127.0.0.1:8999'
# }
#
#
# PAY_STATUS_MAPPING = {
#     "1":"已支付",
#     "-8":"待支付",
#     "0":"已关闭"
# }
#
# PAY_STATUS_DISPLAY_MAPPING = {
#     "0":"订单关闭",
#     "1":"支付成功",
#     "-8":"待支付",
#     "-7":"待发货",
#     "-6":"待确认",
#     "-5":"待评价"
# }