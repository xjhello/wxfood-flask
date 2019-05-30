class Config(object):
    # SERVER_PORT = 8999
    SECRET_KEY = "XHSOI*Y9dfs9cshd9"
    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/wxapi"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENCODING = "utf8mb4"  # 编码

    AUTH_COOKIE_NAME = "mooc_food"  # cookie名称
    # 过滤url
    IGNORE_URLS = [
        "^/user/login",
        "^/api",
    ]

    # 完全不用判断的url
    IGNORE_CHECK_LOGIN_URLS = [
        "^/static",
        "^/favicon.ico"
    ]

    # api访问拦截器忽略
    API_IGNORE_URLS = [
        "^/api",
    ]

    # 域名
    APP = {
        'domain': 'http://127.0.0.1:5000'
    }

    # 上传的图片设置
    UPLOAD = {
        'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
        'prefix_path': '/home/static/upload/',
        'prefix_url': '/static/upload/'
    }

    PAGE_SIZE = 50  # 每页多少条
    PAGE_DISPLAY = 10  # 显示的总页数

    STATUS_MAPPING = {  # 账户状态
        "1": "正常",
        "0": "已删除"
    }

    PAY_STATUS_MAPPING = {
        "1": "已支付",
        "-8": "待支付",
        "0": "已关闭"
    }

    PAY_STATUS_DISPLAY_MAPPING = {
        "0": "订单关闭",
        "1": "支付成功",
        "-8": "待支付",
        "-7": "待发货",
        "-6": "待确认",
        "-5": "待评价"
    }

    # 小程序开发者参数
    MINA_APP = {
        'appid': 'wx3531ec6cb6dce0ef',
        'appkey': 'cf5f6f28d7571d63b4f04bd1fff4765a',
    }

    # redis
    # REDIS_HOST = "127.0.0.1"
    # REDIS_PORT = 6379
    # AUTH_COOKIE_NAME = "mooc_food"  # cookie名称
    # # RELEASE_VERSION = 1
    # # flask-session配置
    # SESSION_TYPE = "redis"
    # SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    # PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位秒


class DevelopmentConfig(Config):
    """开发模式配置信息"""
    DEBUG = True


class ProductConfig(Config):
    """生产环境配置信息"""
    DEBUG = False


config_map = {
    "develop": DevelopmentConfig,
    "product":  ProductConfig
}