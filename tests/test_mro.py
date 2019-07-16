# -*- coding:utf-8 -*-

# 测试类的__mro__属性

# MRO 方法解析顺序, Method Resolution Order
# https://blog.csdn.net/weixin_35653315/article/details/78107466

class A(object):
    def foo(self):
        print('A.foo()')


class B(object):
    def foo(self):
        print('B.foo()')


class C(B, A):
    def foo(self):
        print('C.foo()')


c = C()
c.foo()
print(C.__mro__)
# (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
# 从C.__mro__的值可以看出, Python的方法解析优先级从高到低为:
# 1. 实例本身(instance)
# 2. 类(class)
# 3. super class, 继承关系越近, 越先定义, 优先级越高.
for mro_class in C.__mro__:
    print(mro_class.__dict__)
    print(dir(mro_class))

# 一个小知识点：__dir__和dir的区别：
# https://blog.csdn.net/lis_12/article/details/53521554
# 一句话__dict__是dir的子集，dir列出包括父类在内的所有属性集合__dict__仅仅是自己当前类的属性字典
