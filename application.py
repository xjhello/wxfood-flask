# coding: utf-8
from flask import Flask


# 重载flask对象，配置分步加载
class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):  # 重载初始化方法,重置template位置
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=None)  # 重构,改变template，static等默认值


