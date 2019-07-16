# -*- coding:utf-8 -*-
from datetime import datetime
from urllib.parse import urlparse, urljoin

from bluelog.utils import is_safe_url

print(datetime.utcnow())  # 2019-03-13 02:23:32.096625
print(datetime.now())  # 2019-03-13 10:23:32.096802

print(datetime.now().timestamp())  # 1552443953.565508

target = 'http://47.93.193.222:8002/auth/login?next=%2F%3F'


def is_safe_url(target):
    # url_change = urlparse('https://i.cnblogs.com/EditPosts.aspx?opt=1')
    # 返回结果：ParseResult(scheme='https',netloc='i.cnblogs.com',path=/EditPosts.aspx,params='',query='opt=1',fragment='')
    host_url = 'http://47.93.193.222:8002'
    ref_url = urlparse(host_url)
    test_url = urlparse(urljoin(host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


print(is_safe_url(target))


