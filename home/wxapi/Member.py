"""
api 会员入口
"""
from home import db
from home.libs.Helper import getCurrentDate
from home.libs.member.MemberService import MemberService
from home.models.food.WxShareHistory import WxShareHistory
from home.wxapi import route_api
from flask import request, jsonify, g
from home.models.member.Member import Member
from home.models.member.OauthMemberBind import OauthMemberBind


# 登录入口
@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values  # 得到前端的数据
    # app.logger.info(req)
    code = req['code'] if 'code' in req else ''  # 获取code！
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    # 向微信发送code获取唯一标识openID
    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    # 从前端获取信息(昵称，性别，头像)
    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    # 从绑定表中通过openID查找是否存在，即是否已经注册
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:  # 没有绑定
        # 如果没有绑定，则需要注册到member和关联表中
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()  # 产生随机字符串
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()  # 保存到数据库

        # 注册关联
        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    # 如果已经注册，则返回信息
    member_info = Member.query.filter_by(id=bind_info.member_id).first()  # 则获取详细信息
    # 这里是第一次登陆注册，发票据！！！！
    # app.logger.info(member_info.id)
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)


# 检查是否已经注册(!! 减少每次登陆时传递的参数，第一次登陆注册一些昵称信息就保存在数据库里面了
# 下一次登陆就只要传递code来判断是否已经注册了，昵称等信息就可以在数据库中获取)
@route_api.route("/member/check-reg", methods=["GET", "POST"])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)


# 保存用户分享信息
@route_api.route("/member/share", methods=["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info  # 分享的会员id(拦截器中获得id)
    model_share = WxShareHistory()  # 创建模型
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)


@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname": member_info.nickname,
        "avatar_url": member_info.avatar
    }
    return jsonify(resp)
