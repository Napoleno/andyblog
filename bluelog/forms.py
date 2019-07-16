# -*- coding:utf-8 -*-
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email, Optional, URL

from bluelog.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    author = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField('内容', validators=[DataRequired()])
    category = SelectField('分类', coerce=int)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name.desc()).all()]


class CategoryForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(20)])
    submit = SubmitField()

