from flask import Blueprint

route_api = Blueprint('wxapi', __name__)
from home.wxapi.Member import *
from home.wxapi.Food import *
from home.wxapi.Cart import *
from home.wxapi.Order import *
from home.wxapi.My import *


@route_api.route('/')
def index():
    return 'Hello'