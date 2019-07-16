# -*- coding:utf-8 -*-
import time

from flask import Blueprint, request, current_app, render_template, flash, redirect, url_for, session, abort, \
    make_response
from flask_login import current_user, login_required
from bluelog.extensions import db
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.models import Post, Comment, Category, Link
from bluelog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    current_app.logger.info('session,user_id={}'.format(session.get('user_id', 'no user_id')))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    '''显示博客条目详情'''
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']

    # 知道post，得到post对应所有的comment，这里有好几种方式，可以试一下
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.desc()).paginate(
        page, per_page)

    # 这种写法无法排序
    # pagination = post.comments.filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        # 如果当前用户是管理员admin
        # 隐藏字段赋值
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author=author, email=email, site=site, body=body,
                          from_admin=from_admin, post=post,
                          reviewed=reviewed)
        # 根据reply_comment 这个endpoint的参数
        # replied_id就是对Comment进行reply的Comment的id
        # 这个字段是Comment表中的外键，关联的是主键id
        replied_id = request.args.get('reply')
        if replied_id:
            # 如果这个不为空，则是对comment评论的reply
            replied_comment = Comment.query.get_or_404(replied_id)
            #
            comment.replied = replied_comment

        db.session.add(comment)
        db.session.commit()

        if current_user.is_authenticated:
            flash('评论发表成功', 'success')
        else:
            flash('您的评论将在审核后发布', 'info')
        return redirect(url_for('.show_post', post_id=post_id))
    # else:
    #     flash('form validate not passed!')
    #     return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)


@blog_bp.route('/reply_comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    print('comment.post.can_comment={}'.format(comment.post.can_comment))
    if not comment.post.can_comment:
        # 如果此条评论所在的博客不能评论
        flash('Comment is disabled.', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
        # 重定向到当前页的特殊锚点,并且reply参数，指定的是对哪条comment进行reply
        # url_for之后的就是request的参数:http://47.93.193.222:8002/post/44?reply=86
    return redirect(
        url_for('.show_post', post_id=comment.post.id, author=comment.author, reply=comment_id) + '#comment-form')


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)
    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response


@blog_bp.route('/category/<int:category_id>', methods=['GET', 'POST'])
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('BLUELOG_POST_PER_PAGE', 10)
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, posts=posts, pagination=pagination)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')
