# -*- coding:utf-8 -*-


def generator_honor():
    for i in [1, 3, 4, 5, 12, 3, 4]:
        if i < 4:
            continue
        yield i


# 测试生成器的取值
gen = generator_honor()

# for g in gen:
#     print(g)


print('123'.join(f for f in []) =='')  # 这个是True
