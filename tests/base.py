# -*- coding:utf-8 -*-
import unittest

from flask_wtf import FlaskForm

from bluelog import db, create_app
from bluelog.forms import LoginForm
from wsgi import app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        # http://flask-sqlalchemy.pocoo.org/2.3/contexts/
        self.context = app.app_context()
        self.context.push()
        db.create_all()
        self.runner = app.test_cli_runner()
        self.client = app.test_client()

    def tearDown(self):
        db.drop_all()
        # 测试结束，销毁应用上下文对象
        self.context.pop()

