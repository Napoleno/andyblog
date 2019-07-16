# -*- coding:utf-8 -*-
class LoginManager(object):

    def __init__(self):
        self.user_callback = None

    def user_loader(self, callback):
        self.user_callback = callback
        callback()
        return callback
