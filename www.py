from home.api.chart import route_chart
from home.api.finance.Finance import route_finance
from home.api.food.Food import route_food
from home.api.stat.Stat import route_stat
from home.api.upload.Upload import route_upload
from home.api.user import route_user
from home.api.static import route_static
from home.api.index import route_index
from home.api.account.Account import route_account
from home.api.member.Member import route_member
from home.wxapi import route_api
# 统一拦截处理和统一错误处理
# from web.interceptors.ApiAuthInterceptor import  *
# from web.interceptors.ErrorInterceptor import *
from home.interceptors.AuthInterceptor import *

# 注册蓝图到app


app.register_blueprint(route_index, url_prefix="/")  # 主页面
app.register_blueprint(route_user, url_prefix="/user")  # 用户
app.register_blueprint(route_static, url_prefix="/static")  # 静态资源引用
app.register_blueprint(route_account, url_prefix="/account")  # 后台账户管理模块
app.register_blueprint(route_stat, url_prefix="/stat")  # 统计
app.register_blueprint(route_finance, url_prefix="/finance")  # 财务
app.register_blueprint(route_member, url_prefix="/member")  # 会员
app.register_blueprint(route_food, url_prefix="/food")  # 食物
app.register_blueprint(route_api, url_prefix="/api")  # 小程序api
app.register_blueprint(route_upload, url_prefix="/upload")  # 上传图片url
app.register_blueprint(route_chart, url_prefix="/chart")
