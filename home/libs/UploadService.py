"""
图片上传封装方法
"""
from werkzeug.utils import secure_filename
from home import app, db
from home.libs.Helper import getCurrentDate
import datetime
import os, stat, uuid
from home.models.Image import Image


class UploadService():
    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[1]  # 文件扩展(.jpg  .mp3)
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = "不允许的扩展类型文件"
            return resp

        root_path = app.root_path + config_upload['prefix_path']  # 存放上传文件的路径
        # 不使用getCurrentDate创建目录，为了保证其他写的可以用，这里改掉，服务器上好像对时间不兼容
        file_dir = datetime.datetime.now().strftime("%Y%m%d")  # 按日期生成文件夹
        save_dir = root_path + file_dir  # 组合成路径
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        file_name = str(uuid.uuid4()).replace("-", "") + "." + ext
        file.save("{0}/{1}".format(save_dir, file_name))

        model_image = Image()
        model_image.file_key = file_dir + "/" + file_name
        model_image.created_time = getCurrentDate()
        db.session.add(model_image)
        db.session.commit()

        resp['data'] = {
            'file_key': model_image.file_key
        }
        return resp
