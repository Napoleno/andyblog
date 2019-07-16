# -*- coding:utf-8 -*-

# 类中的全局标量和对象中的变量的区别

class UnboundField(object):
    creation_counter = 0

    def __init__(self):
        UnboundField.creation_counter += 1
        self.creation_counter = UnboundField.creation_counter


u1 = UnboundField()
print(u1.creation_counter)  # 1
u2 = UnboundField()
print(u2.creation_counter)  # 2
print(UnboundField.creation_counter)  # 2

L = [2, 4, 5, 1, 66, 33, 11, 0]
d = dict(a=1, b=2)

print(hasattr(L, 'items'))
print(hasattr(d, 'items'))
print(d.items())
