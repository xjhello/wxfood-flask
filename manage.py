from home import db, app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from home.libs.UrlManager import UrlManager
import www
# 函数模板：将方法注入到模板中
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildImageUrl, 'buildImageUrl')  # 图片路径

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
