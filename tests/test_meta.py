# -*- coding:utf-8 -*-

# type子类的__init__和_call__方法的调用顺序研究，以及参数的研究
# 创建FlaskForm对象之前会先实例化FormMeta类调用__init__方法，之后再调用__call__方法
from typing import Any


class A:

    def __new__(cls, *args, **kwargs):
        print('A,__new__')
        return super(A, cls).__new__(cls, *args, **kwargs)

    def __init__(self, name=None):
        super(A, self).__init__()
        print('A,__init__')


class B:
    def __new__(cls, *args, **kwargs):
        print('B,__new__')
        return super(B, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super(B, self).__init__()
        print('B,__init__')


class FormMeta(type):

    def __init__(cls, what, bases=None, dict=None):
        # cls:当前类对象FlaskForm  <class '__main__.FlaskForm'>
        # what:当前类对象的名字FlaskForm  字符串   'FlaskForm'
        # bases：当前类对象的父类 是一个元组 <class 'tuple'>: (<class '__main__.BaseForm'>,)
        # dict：当前类对象的属性 是一个字典  <class 'dict'>: {'__qualname__': 'FlaskForm', '__module__': '__main__', '__init__': <function FlaskForm.__init__ at 0x7fca19179a60>, 'foo': <function FlaskForm.foo at 0x7fca19179ae8>}
        print('FormMeta,__init__')
        super(FormMeta, cls).__init__(what, bases, dict)

    def __call__(cls, *args, **kwargs):
        print('FormMeta,__call__')
        return super(FormMeta, cls).__call__(*args, **kwargs)


class BaseForm:
    pass


class FlaskForm(BaseForm, metaclass=FormMeta):

    def __init__(self):
        print('FlaskForm,__init__')

    def __call__(self, *args, **kwargs):
        print('FlaskForm,__call__')

    def foo(self):
        print('form.foo()')

    a = A()
    b = B()


f = FlaskForm()
