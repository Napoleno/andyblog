# -*- coding:utf-8 -*-

# https://www.cnblogs.com/goldsunshine/p/9269880.html
import time
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from bluelog.extensions import db


class Company(db.Model):
    __tablename__ = 'company'
    name = db.Column(db.String(20), primary_key=True)
    location = db.Column(db.String(40))
    phones = db.relationship('Phone', backref='phone_of_company', lazy=True)


class Phone(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20))
    price = db.Column(db.String(30))
    company_name = db.Column(db.String(20), ForeignKey('company.name'))
    # company = db.relationship('Company', backref='phones')


class Admin(db.Model, UserMixin):
    """用户类"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self) -> str:
        return 'username={}'.format(self.username)


class Category(db.Model):
    """博客分类"""
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    # category.posts  知道category求category下所有的post
    # post.post_of_category 知道post，求post所在的category
    posts = db.relationship('Post', back_populates='category', cascade='all,delete-orphan')


class Post(db.Model):
    """博客条目"""
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), )
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    can_comment = db.Column(db.Boolean, default=True)

    # Category:Post=One:Many 一对多关系 Post中含有Category的外键
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    # Post.comments  知道post求post下所有的comments
    # comment.comment_of_post 知道comment，求comment对应的post
    comments = db.relationship('Comment', back_populates='post', cascade='all,delete-orphan')

    def __str__(self) -> str:
        return self.title


class Comment(db.Model):
    """每条博客的评论"""
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    email = db.Column(db.String(254))
    # site表示发布comment的作者的个人网站
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    # 是否是自己评论
    from_admin = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)

    # Post:Comment=One:Many 一对多关系 Comment中含有Post的外键
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    # 评论审查是否通过
    reviewed = db.Column(db.Boolean, default=False)

    # 得到评论的回复列表，此字段在项目中没有用到
    # replies = db.relationship('Comment', lazy='select',
    #                           backref=db.backref('replied', remote_side=[id]),
    #                           cascade='all,delete-orphan')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')

    # 还有一种特殊的评论，这种评论是对评论的评论，我暂且叫他回复
    # 假如还有一个表叫Reply
    # Comment:Reply=One:Many  回复同时也是一种特殊的评论，引用自己的主键，叫自关联
    # replied_id:表示对那个comment进行的回复
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 根据post.html的理解，此字段表示当前reply是对那个comment的回答，这个是特殊的comment
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


class Link(db.Model):
    """链接"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
# 表的级联关系
# Category:Post=one:many
# Post:Category=one:many
# Comment:Comment=One:Many
