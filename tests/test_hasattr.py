# -*- coding:utf-8 -*-

# 测试对象的hasattr和getattr方法
d = dict(a=0)

print(dir(d))
print(hasattr(d, 'get'))
print(getattr(d, 'get'))
