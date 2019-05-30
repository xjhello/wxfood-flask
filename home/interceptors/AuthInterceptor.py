"""
拦截器，用于拦截需要登录的页面请求
"""
import re
from flask import request, g, redirect
from home.libs.UrlManager import UrlManager
from home.libs.UserService import UserService
from home.models.user.User import User
from manage import app


@app.before_request
def before_request():
    # 不需要验证登录的url
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']

    path = request.path  # 得到请求的url

    # 如果是静态文件就不要查询用户信息了
    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))  # 正则表达式提取url，如果在配置忽略过滤中就直接返回
    if pattern.match(path):
        return

    # 如果是规定的忽略url(如api)就不要拦截
    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return

    user_info = check_login()  # 检查是否登录，在下面定义了
    g.current_user = None  # flask的g变量用于记录用户登录标识(临时的)
    if user_info:
        g.current_user = user_info  # 用户已经登录，改变为用户id

    # 加入日志。这里的逻辑说明是管理员了，就要把每一次需要权限的操作记录保存
    # LogService.addAccessLog()

    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))

    return


'''
判断用户是否已经登录
'''


def check_login():  # 根据cookie信息判断是否登录
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None

    if '/api' in request.path:
        app.logger.info(request.path)
        auth_cookie = request.headers.get("Authorization")
        app.logger.info(request.headers.get("Authorization"))

    if auth_cookie is None:  # cookie不存在
        return False

    auth_info = auth_cookie.split("#")  # 将cookie以#切割形成list
    if len(auth_info) != 2:  # 0为授权码 1为uid （cookie中只有这两个信息）
        return False
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()  # 查找用户信息
    except Exception:
        return False

    if user_info is None:  # 差不多uid
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):  # 授权码不相同
        return False

    if user_info.status != 1:  # 判断管路员状态，已经删除的要立即退出
        return False

    return user_info
