# -*- coding: utf-8 -*-
"""
url 管理
"""
import time
from home import app


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        # release_version = app.config.get('RELEASE_VERSION')  # 版本号
        # ver = "%s" % (int(time.time())) if not release_version else release_version
        path = "/static" + path
        return UrlManager.buildUrl(path)

    @staticmethod  # 上传的图片访问url
    def buildImageUrl(path):
        app_config = app.config['APP']
        url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
        return url
