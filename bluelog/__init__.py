# -*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

import os

import click
from flask import Flask, current_app
from flask_sqlalchemy import get_debug_queries
from sqlalchemy.exc import IntegrityError
from bluelog.extensions import db, bootstrap, login_manager, moment, csrf_protect, ckeditor
from bluelog.blueprints import auth
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.blueprints.test_blueprint import test_bp

from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links
from bluelog.models import Company, Phone, Admin, Category, Link, Post, Comment
from bluelog.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print('basedir=' + basedir)


def create_app(config_name):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)

    # app.config.from_pyfile('settings.py')
    app.config.from_object(config[config_name])

    # 参见官方文档：https://docs.python.org/3.7/library/logging.html?highlight=logging#handler-objects
    register_logging(app)
    # 注册（初始化扩展包）
    register_extensions(app)
    # 注册blueprint
    register_blueprints(app)
    # 注册Flask的命令行模块
    register_commands(app)
    # 注册模板中使用的全局变量
    register_template_context(app)
    # 注册函数查询记录信息
    register_request_handlers(app)
    return app


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= current_app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
                print('Slow query:Duration :%fs\n Context:%s\nQuery:%s\n' % (q.duration, q.context, q.statement))
            # 下边打log会报错
            # app.logger.debug('duration=get_debug_queries')
        return response


def register_logging(app):
    # log文件10M，可以存10次
    # https://docs.python.org/3.7/library/logging.handlers.html#rotatingfilehandler
    file_handler = RotatingFileHandler(filename=os.path.join(basedir, 'logs/bluelog.log'), mode='a',
                                       maxBytes=1024 * 1024 * 10,
                                       backupCount=10,
                                       encoding='utf-8')
    # fmt是自定义打印信息，具体结构见：http://www.cnblogs.com/i-honey/p/8052579.html
    # 其中message显示的内容才是我们在项目中调用logger.debug()输出的内容
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    # 规定上边的fmt中asctime的格式
    datefmt = '[%Y-%m-%d %H:%M:%S]'
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    if not app.debug:
        # http://flask.pocoo.org/docs/1.0/api/?highlight=flask#module-flask
        app.logger.addHandler(file_handler)


def register_blueprints(app):
    app.register_blueprint(test_bp, url_prefix='/test')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/blog')


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    # toolbar.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    csrf_protect.init_app(app)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        # 当前登录的用户
        admin = Admin.query.first()
        # 侧边栏展示的所有的博客分类
        categories = Category.query.order_by(Category.name).all()
        # 侧边栏展示的所有的链接
        links = Link.query.order_by(Link.name).all()
        return dict(admin=admin, categories=categories, links=links)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def init_db(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def forge():
        # 下面的这两句代码是必须的
        db.drop_all()
        db.create_all()

        from tests.datas import companys
        from tests.datas import phones

        for key, value in companys.items():
            company = Company(name=key, location=value)
            db.session.add(company)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        click.echo('写入公司信息成功...')
        for phone in phones:
            phone = Phone(id=phone[0], model=phone[1], price=phone[3], company_name=phone[2])
            db.session.add(phone)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        click.echo('写入电话信息成功...')

        phone = Phone(id=7, model='Blackberry', price=5987, company_name='RIM')
        db.session.add(phone)
        db.session.commit()

    @app.cli.command()
    @click.option('--company', default='Apple', help='delete company by name.')
    def delete_company(company):
        c = Company.query.filter_by(name=company).first()
        db.session.delete(c)
        db.session.commit()

    @app.cli.command()
    def get_location_by_model():
        # many-->ones
        # 方式一：未使用relationship()方法的，查表求：已知一个手机型号（model）是xiaomi2s,求生产这个手机的公司的地址
        # 步骤一：由手机得到手机跟公司关联的外键
        # 步骤二：由这个外键得到公司，进而得到公司的地址
        phone = Phone.query.filter_by(model='xiaomi2s').first()
        company = Company.query.filter_by(name=phone.company_name).first()
        click.echo('生产xiaomi2s的公司地址是{}'.format(company.location))

        # 方式二：
        # 使用relationship的方式
        phone = Phone.query.filter_by(model='xiaomi2s').first()
        click.echo('生产xiaomi2s的公司地址是{}'.format(phone.phone_of_company.location))

        # 方式三：嵌套查询
        resultProxy = db.session.execute(
            'select company.name,company.location from company where company.name=(select phone.company_name from phone where phone.[model]="xiaomi2s")')
        for rowProxy in resultProxy:
            for tup in rowProxy.items():
                click.echo(tup)

        # click.echo('生产xiaomi2s的公司地址是{}'.format(companys[0].location if len(companys) > 0 else '未查到'))

    @app.cli.command()
    def get_phone_by_company():
        # 给定公司得到他所有的手机  one-->many
        # 方式一：
        # with_parent跟relationship正好相反
        phones = Phone.query.with_parent(Company.query.filter_by(name='Apple').first())
        for phone in phones:
            click.echo(phone.model)

        # 方式二：
        phones = Company.query.filter_by(name='Apple').first().phones
        for phone in phones:
            click.echo(phone.model)

    @app.cli.command()
    @click.option('--category', default=10, help='add category')
    @click.option('--post', default=50, help='add post')
    @click.option('--comment', default=500, help='add comment')
    # @click.option('--link', help='add comment')
    def forge_new(category, post, comment):

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories()

        click.echo('Generating %d posts...' % post)
        fake_posts()

        click.echo('Generating %d comments...' % comment)
        fake_comments()

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')

    @app.cli.command()
    def get_phones_of_company():
        # phones = Company.query.filter_by(name='Apple').first().phones
        # click.echo('phones={}'.format(phones))
        phones = Company.query.filter_by(name='Apple').first().phones
        for phone in phones:
            click.echo(phone.model)

    @app.cli.command()
    def all_post_can_comment():
        '''更改所有的博客都可以评论'''
        posts = Post.query.all()
        for post in posts:
            post.can_commend = True
        db.session.commit()

    @app.cli.command()
    def get_replies():
        comment = Comment.query.get(86)
        comments = comment.replies
        for reply in comments:
            click.echo('reply={}'.format(reply.author))



