# -*- coding: utf-8 -*-
"""
会员的一些方法封装
"""
import hashlib, requests, random, string, json

from manage import app


class MemberService():
    # 产生token
    @staticmethod
    def geneAuthCode(member_info=None):
        m = hashlib.md5()
        # 用户id，用户salt字段(随机)，用户状态字段
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    # 产生随机字符串
    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))

    # 获取openID
    @staticmethod
    def getWeChatOpenId(code):
        # 向微信发送code获取唯一标识openID
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        r = requests.get(url)  # 得到返回结果
        res = json.loads(r.text)  # 序列化为json
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid
