# -*- coding: utf-8 -*-
"""
user 公用的一些核心操作方法
"""
import hashlib, base64, random, string


class UserService():  # 产生加密用户信息 存入到cookie
    @staticmethod
    def geneAuthCode(user_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):  # 产生加密密码
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()  # 16进制的编码

    @staticmethod  # 管理员的产生随机字符串
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))
