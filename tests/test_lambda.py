# -*- coding:utf-8 -*-

# python中的lambda表达式
# 分为无参表达式和有参数表达式

def connect(params):
    print('connect...' + params)


def generate_csrf(secret_key=None, token_key=None):
    print('generate_csrf')


class Engine():
    def __init__(self, f):
        self._f = f

    def exe_f(self, params):
        self._f(params)


def context_processor(f):
    print('context_processor...')
    result = f()
    print('result={}'.format(result))


if __name__ == '__main__':
    # e = Engine(lambda: connect('你好'))
    # e = Engine(connect)
    # e.exe_f('零零零零')
    pass
    # context_processor(generate_csrf)
    context_processor(lambda: {'csrf_token': generate_csrf})

    l = [2, 4, 1, 7, 4, 33, 55, 22]

    l.sort(key=lambda x: (x, 4))
    print(l)
