# -*- coding:utf-8 -*-
import unittest

from collections import Iterable

from bluelog.forms import LoginForm
from tests.base import BaseTestCase


class BlogTestCase(BaseTestCase):
    def test_create_comment(self):
        response = self.client.post('/post/44?reply=86', data=dict(
            name='andy',
            email='napoleno_1987@163.com',
            site='www.baidu.com',
            body='comment123',
            from_admin=False,
            reviewed=False), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Thanks, your comment will be published after reviewed.', data)

    def test_getattr(self):
        '''测试LoginForm中使用getattr（username）返回的是什么类型'''
        f = LoginForm()
        print('test_getattr={}'.format(getattr(f, 'username').__str__))
        print('test_getattr={}'.format(type(getattr(f, 'username')).__str__))

    def test_mro(self):
        '''测试类的父类继承关系'''
        for mro_class in LoginForm.__mro__:
            print(mro_class)

    def test_field_in_form(self):
        f = LoginForm()
        print(isinstance(f, Iterable))
        for field in f:
            print(str(field))


if __name__ == '__main__':
    unittest.main()
