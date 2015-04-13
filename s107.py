__author__ = 'sail'
import pandas as pd
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt


def analyse():
    # 该函数用于将一个dataFrame合并为一条记录
    # 入参x为一个dataFrame，调用tt对每个Series分别进行合并
    def t(x):
        return x.apply(tt)

    # 该函数用于对一个Series进行合并,入参x为一个Series
    def tt(x):
        # 当x为标题时用reduce调用lcs函数求从字符串头开始的最长公共子串
        if x.name == '标题':
            return reduce(lcs, x)
        # 当x为下列内容是取最后一项
        elif x.name in {'日期', '粉丝数'}:
            return x[-1]
        # 其他情况时对将x中所有数据合并为一组求和，并返回该组求和结果
        else:
            return x.groupby(lambda x: 1).sum().values[0]

    def lcs(x, y):
        for i in range(min(len(y), len(x))):
            if x[i] != y[i]:
                break
        else:
            i += 1
        return x[:i]

    df = pd.ExcelFile(r"resource/wxgzhdata.xlsx").parse(u"3月")
    df.insert(0, '标题', df['文章标题'])
    df = df.fillna(method="pad").dropna().set_index(['文章标题']).groupby(lambda x: x[:2]).apply(lambda x: x.apply(
        lambda y: {1: lambda z: reduce(lcs, z), 2: lambda z: z[-1], None: lambda z: z.groupby(type).sum().values[0]}
        [{'标题': 1, '日期': 2, '粉丝数': 2}.get(y.name)](y))).set_index(['标题'])
    # 下面为上句的另一种表达方式
    # 用fillna填充nan
    # df=df.fillna(method="pad")
    # 将开头未能被pad填充的nan去除
    # df=df.dropna()
    # 将标题设为index以方便分组
    # df=df.set_index(['文章标题'])
    # 以标题的前两个字为基准分组
    # df=df.groupby(lambda x: x[:2])
    # 利用函数t对每个groupBy进行合并
    # df=df.apply(t)
    # 将各系列内文章标题的相同部分作为系列名称
    # df=df.set_index(['标题'])

    # 从dataframe中取得之后计算需要的Series
    fields = [df.xs('总阅读人数', axis=1), df.xs('初次打开阅读人数', axis=1), df.xs('分享次数', axis=1), df.xs('每日增粉人数', axis=1),
              df.xs('粉丝数', axis=1)]
    to_percent = lambda x: (x * 100).round(1)
    # 各字段计算公式
    expressions = [('初次打开率', lambda f: f[1] / f[4]), ('分享率', lambda f: f[2] / f[0]), ('分享拉粉率', lambda f: f[3] / f[2]),
                   ('增粉速率', lambda f: f[3] / f[4]), ( '阅读涨粉率', lambda f: f[3] / f[0]),
                   ('传播涨粉率', lambda f: f[3] / (f[0] - f[1])), ('二次传播率', lambda f: (f[0] - f[1]) / f[0])]
    # 记录现有字段数量，用于下面计算新字段插入位置以及删除旧字段。
    old_field_count = len(df.columns)
    # 计算各字段的值，处理为percent后，依次插入datagrame中
    for i in enumerate(expressions, start=old_field_count):
        df.insert(i[0], i[1][0], (i[1][1](fields)).apply(to_percent))
    # 转制后将原始字段去除
    df = df.T[old_field_count:]

    df.plot(kind='barh', figsize=(16, 9))

    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.show()