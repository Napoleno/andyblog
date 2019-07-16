# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from bluelog.models import Post, Category, Link, Comment
from bluelog.extensions import db
from bluelog.forms import SettingForm, PostForm, CategoryForm, LinkForm
from bluelog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('管理员信息提交成功', 'success')
        return redirect(url_for('blog.index'))
        # 回显
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, int)
    per_page = current_app.config.get('BLUELOG_MANAGE_POST_PER_PAGE', 10)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', posts=posts, pagination=pagination, page=page)


@admin_bp.route('edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    '''编辑博客的条目'''
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category.name = form.category.default
        return redirect(url_for('blog.show_post'))

    form.title.data = post.title
    form.body.data = post.body
    form.category.default = post.category.name
    return render_template('admin/edit_post.html', form=form, )


@admin_bp.route('post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    '''删除博客条目'''
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect_back()


@admin_bp.route('post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        # category是绑定的category的id
        category_id = form.category.data
        post = Post(title=title, body=body, category_id=category_id)
        db.session.add(post)
        db.session.commit()
        flash('新建文章成功', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('category/manage', methods=['GET', 'POST'])
@login_required
def manage_category():
    page = request.args.get('page', 1, int)
    per_page = current_app.config.get('BLUELOG_MANAGE_CATEGORY_PER_PAGE', 10)
    pagination = Category.query.order_by(Category.name.desc()).paginate(page, per_page=per_page)
    categories = pagination.items
    return render_template('admin/manage_category.html', categories=categories)


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('新建分类成功', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin.manage_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('删除分类成功', 'success')
    return redirect(url_for('admin.manage_category'))


@admin_bp.route('link/manage')
@login_required
def manage_link():
    links = Link.query.order_by(Link.name.desc()).all()
    return render_template('admin/manage_link.html', links=links)


@admin_bp.route('link/new', methods=['POST', 'GET'])
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(name=form.name.data, url=form.url.data)
        db.session.add(link)
        db.session.commit()
        flash('更新成功', 'success')
        return redirect(url_for('admin.manage_link'))
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('link/<int:link_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_link(link_id):
    link = Link.query.get_or_404(link_id)
    form = LinkForm()
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.add(link)
        db.session.commit()
        flash('更新成功', 'success')
        return redirect(url_for('admin.manage_link'))
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin.manage_link'))


@admin_bp.route('comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')
    if filter_rule == 'unread':
        filter_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filter_comments = Comment.query.filter_by(from_admin=True)
    else:
        filter_comments = Comment.query
    page = request.args.get('page', 1, int)
    per_page = current_app.config.get('BLUELOG_MANAGE_MANAGE_PER_PAGE', 10)
    pagination = filter_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('comment/<int:comment_id>/approve/', methods=['POST'])
@login_required
def approve_comment(comment_id):
    """审查评论"""
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.add(comment)
    db.session.commit()
    flash('评论审查通过', 'success')
    return redirect_back()


@admin_bp.route('comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功', 'success')
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
def set_comment(post_id):
    """设置当前文章是否可以评论"""
    post = Post.query.get_or_404(post_id)
    # request.full_path=/admin/post/53/set-comment?next=%2Fblog%2Fpost%2F53%3F
    current_app.logger.debug('request.full_path={}'.format(request.full_path))
    if post.can_comment:
        post.can_comment = False
    else:
        post.can_comment = True
    db.session.add(post)
    db.session.commit()
    flash('操作成功', 'success')
    return redirect_back()
