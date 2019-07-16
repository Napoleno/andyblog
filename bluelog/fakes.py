# -*- coding:utf-8 -*-
# 数据库中插入模拟数据
import random

from sqlalchemy.exc import IntegrityError

from bluelog import db
from bluelog.models import Admin, Category, Post, Comment, Link
from faker import Faker

fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        name='AndyZhang',
        blog_title='Bluelog',
        blog_sub_title="No, I'm the real thing.",
        about='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...')
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(),
            timestamp=fake.date_time_this_year(),
            category_id=Category.query.get(random.randint(1, Category.query.count())).id)
        db.session.add(post)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_comments(count=500):
    for i in range(count):
        # 添加审查通过的comment
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.text(),
            timestamp=fake.date_time_this_year(),
            post_id=Post.query.get(random.randint(1, Post.query.count())).id,
            reviewed=True
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 添加未审查通过的comment
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.text(),
            timestamp=fake.date_time_this_year(),
            post_id=Post.query.get(random.randint(1, Post.query.count())).id,
            reviewed=False
        )
        db.session.add(comment)
        # from  admin
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.text(),
            timestamp=fake.date_time_this_year(),
            post_id=Post.query.get(random.randint(1, Post.query.count())).id,
            reviewed=False,
            from_admin=True
        )
        db.session.add(comment)

    for i in range(salt):
        # replies
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.text(),
            timestamp=fake.date_time_this_year(),
            post_id=Post.query.get(random.randint(1, Post.query.count())).id,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            reviewed=False,
            from_admin=True
        )
        db.session.add(comment)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
