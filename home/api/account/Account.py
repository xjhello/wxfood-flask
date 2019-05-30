from flask import Blueprint, request, redirect, jsonify
from sqlalchemy import or_
from home import db
from home.libs.Helper import iPagination, ops_render, getCurrentDate
from home.libs.UrlManager import UrlManager
from home.libs.UserService import UserService
from home.models.user.User import User
from manage import app

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1  # 取请求中的页数
    query = User.query  # 表查询对象

    if 'mix_kw' in req:  # 查询字段(混合查询)
        # 使用插件sqlalchemy的 or
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    # 未删除的账户
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    page_params = {
        'total': query.count(),  # 查询总共有多少条数据
        'page_size': app.config['PAGE_SIZE'],  # 每页有多少条
        'page': page,  # 当前页数
        'display': app.config['PAGE_DISPLAY'],  # 显示多少页
        'url': request.full_path.replace("&p={}".format(page), "")  # 每一页url地址
    }

    pages = iPagination(page_params)  # 生成页数

    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    # offset偏移量，list为结果集
    list = query.order_by(User.uid.desc()).all()[offset:limit]  # 分页计算

    resp_data['list'] = list  # 结果集，即循环数据
    resp_data['pages'] = pages  # 分页数据
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("account/index.html", resp_data)


# 会员页面根据传递的id显示用户信息
@route_account.route("/info")
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id', 0))  # 得到id！
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:  # 如果id错误回到列表页面
        return redirect(reback_url)

    info = User.query.filter_by(uid=uid).first()  # 查询id是否存在
    if not info:
        return redirect(reback_url)

    # access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
    resp_data['info'] = info
    # resp_data['access_list'] = access_list
    return ops_render("account/info.html", resp_data)


# 添加账户和编辑修改账户
@route_account.route("/set", methods=["GET", "POST"])
def set():
    default_pwd = "******"
    # print('#'*50)
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id", 0))
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).first()
        resp_data['info'] = info
        return ops_render("account/set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify(resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~"
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~"
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名~~"
        return jsonify(resp)

    if login_pwd is None or len(email) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录密码~~"
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该登录名已存在，请换一个试试~~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    if login_pwd != default_pwd:
        if user_info and user_info.uid == 1:
            resp['code'] = -1
            resp['msg'] = "该用户是演示账号，不准修改密码和登录用户名~~"
            return jsonify(resp)

        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)

    model_user.updated_time = getCurrentDate()  # 获取当前时间
    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)


#  删除和恢复管理员操作
@route_account.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''  # 获取动作
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in ['remove', 'recover']:  # 删除恢复两种操作
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在~~"
        return jsonify(resp)

    if act == "remove":  # 删除
        user_info.status = 0
    elif act == "recover":  # 恢复
        user_info.status = 1

    if user_info and user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "该用户是演示账号，不准操作账号~~"
        return jsonify(resp)

    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
