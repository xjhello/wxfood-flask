import json
from flask import request, jsonify, make_response, redirect, g
from home import db
from home.libs.UrlManager import UrlManager
from home.libs.UserService import UserService
from home.libs.Helper import ops_render
from manage import app
from . import route_user
from home.models.user.User import User


@route_user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return ops_render('user/login.html')

    resp = {'code': 200, 'msg': '登录成功', 'data': {}}  # 返回值
    # 获取前端post过来的数据
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确用户名'
        return jsonify(resp)

    if login_pwd is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确密码'
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()  # 根据name在数据库查找到用户对象
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名和密码-1~~"
        return jsonify(resp)

# 比对密码，user_info.login_salt为加密秘钥，把明文密码加密处理再比对数据库
    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名和密码-2~~"
        return jsonify(resp)

    response = make_response(json.dumps({'code': 200, 'msg': '登录成功~~'}))  # 返回头
    # 设置cookie传到浏览器，AUTH_COOKIE_NAME是cookie名称，传入加密后的字符串和
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
        UserService.geneAuthCode(user_info), user_info.uid), 60 * 60 * 24 * 120)  # 保存120天
    return response


@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return ops_render("user/edit.html", {'current': 'edit'})

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values  # 获取前端的数据
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~"
        return jsonify(resp)

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
    # return ops_render("user/edit.html")


@route_user.route("/reset-pwd", methods=["GET", "POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render("user/reset_pwd.html", {'current': 'reset-pwd'})

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的原密码~~"
        return jsonify(resp)

    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码~~"
        return jsonify(resp)

    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "请重新输入一个吧，新密码和原密码不能相同哦~~"
        return jsonify(resp)

    user_info = g.current_user

    if user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "该用户是演示账号，不准修改密码和登录用户名~~"
        return jsonify(resp)

    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)

    db.session.add(user_info)
    db.session.commit()

    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
        UserService.geneAuthCode(user_info), user_info.uid), 60 * 60 * 24 * 120)  # 保存120天
    return response
    # return ops_render("user/reset_pwd.html")


@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))  # 返回到登录页面
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])  # 删除cookie
    return response
