# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, flash, url_for, redirect, current_app, session, g
from flask_login import login_user, current_user, logout_user, login_required

from bluelog.forms import LoginForm
from bluelog.models import Admin
from bluelog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


# 47.93.193.222:8000/blog

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    # current_app.logger.info('session,csrf_token={}'.format(session.get('csrf_token', 'no csrf_token')))
    # current_app.logger.info('g,csrf_token={}'.format(g.csrf_token if hasattr(g, 'csrf_token') else "no csrf_token"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                # 用户登录成功
                login_user(admin, remember)
                # session.permanent = True
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('错误的用户名或者密码', 'warning')
        else:
            flash('没有账户', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
