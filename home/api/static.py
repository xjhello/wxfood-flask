"""
用于模板能够加载静态文件资源
"""
from flask import Blueprint, send_from_directory

from manage import app

route_static = Blueprint('static', __name__)


@route_static.route("/<path:filename>")
def index(filename):
    return send_from_directory(app.root_path + "/home/static", filename)