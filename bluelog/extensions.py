# -*- coding:utf-8 -*-
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
# toolbar = DebugToolbarExtension()
login_manager = LoginManager()
csrf_protect = CsrfProtect()
ckeditor = CKEditor()
moment = Moment()


# flask-login模块的回调
@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


# 配置flask-login的登录过程
# http://www.pythondoc.com/flask-login/#id1
login_manager.login_view = "auth.login"  # 未登录时，重定向的view
login_manager.login_message = "请登录"
login_manager.login_message_category = "info"
