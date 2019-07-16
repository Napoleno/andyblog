# -*- coding:utf-8 -*-
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    # url_change = urlparse('https://i.cnblogs.com/EditPosts.aspx?opt=1')
    # 返回结果：ParseResult(scheme='https',netloc='i.cnblogs.com',path=/EditPosts.aspx,params='',query='opt=1',fragment='')
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

