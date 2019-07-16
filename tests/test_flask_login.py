# -*- coding:utf-8 -*-
from tests.login_manager_ import LoginManager

login_manager_ = LoginManager()


@login_manager_.user_loader
def load_user():
    print('load_user')


cookie = u'1|5ee3b4681d12f51be216c5273ffac96da334c6d43d2e28abad148b1f44dc9f4d5920abdef6331e1a56825bd4f0f2e5e00032a4c4c86904a3f8b87fa20e04e2f5'

payload, digest = cookie.rsplit(u'|', 1)

print('payload={}'.format(payload))
print('digest={}'.format(digest))

if __name__ == '__main__':
    load_user()
