# -*- coding:utf-8 -*-
import datetime
import sys

import os

# 项目的根目录 /home/andy/flask_projects/bluelog
basedir = os.path.dirname(os.path.dirname(__file__))
WIN = sys.platform.startswith('WIN')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

SQLALCHEMY_TRACK_MODIFICATIONS = False


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置sqlalchemy数据库的路径
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'date_dev.db'))
    # 每页的blog的数量
    BLUELOG_POST_PER_PAGE = 10
    # 每个item的blog的评论数量
    BLUELOG_COMMENT_PER_PAGE = 10
    # _sidebar.html模板中需要的是字典：theme_name：display_name
    BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    # 数据库查询的耗时阈值
    BLUELOG_SLOW_QUERY_THRESHOLD = 1
    # 管理界面展示post时每页的数量
    BLUELOG_MANAGE_POST_PER_PAGE = 10
    # 管理界面展示category时每页的数量
    BLUELOG_MANAGE_CATEGORY_PER_PAGE = 10
    # 管理界面展示comment时每页的数量
    BLUELOG_MANAGE_MANAGE_PER_PAGE = 10

    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=1)
    # REMEMBER_COOKIE_DURATION = 10

    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)
    # PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=10)


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'date_dev.db'))
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
