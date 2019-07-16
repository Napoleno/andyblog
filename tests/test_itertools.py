# -*- coding:utf-8 -*-

# 测试itertools模块
# https://docs.python.org/3/library/itertools.html?highlight=itertools
import itertools

from collections import Iterable

l1 = ['a', 'd', 'e']
l2 = [1, 2, 3]
# 1）可迭代对象包含迭代器。
# 2）如果一个对象拥有__iter__方法，其是可迭代对象；如果一个对象拥有next方法，其是迭代器。
# 3）定义可迭代对象，必须实现__iter__方法；定义迭代器，必须实现__iter__和next方法。

print(isinstance(l1, Iterable))
print(isinstance('abc', Iterable))

print(itertools.chain(l1, l2))
for i in itertools.chain(l1, l2):
    print(i)
