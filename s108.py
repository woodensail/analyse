__author__ = 'sail'
import pandas as pd
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt


def analyse():
    def lcs(x, y):
        for i in range(min(len(y), len(x))):
            if x[i] != y[i]:
                break
        else:
            i += 1
        return x[:i]

    df = pd.ExcelFile(r"resource/wxgzhdata.xlsx").parse(u"3月")
    df = df.fillna(method="pad").dropna()
    df.insert(0, '标题', list(map(lambda x:x[:2],df['文章标题'])))
    df.insert(len(df.columns), '距下一篇的天数', df['文章标题'])
    df = df.fillna(method="pad").dropna().set_index(['文章标题']).groupby(level =0).apply(lambda x: x.apply(
        lambda y: {1: lambda z: z[-1],2:lambda z:len(z), None: lambda z: z.groupby(type).sum().values[0]}
        [{'标题': 1, '日期': 1, '粉丝数': 1,'距下一篇的天数':2}.get(y.name)](y))).sort(['日期'])#.set_index(['标题'])
    # for i in range(len(df['距下一篇的天数'])-1,0,-1):
    #     df['距下一篇的天数'][i]=df['距下一篇的天数'][i-1]
    day_list=list(df['距下一篇的天数'].values)
    day_list.insert(0,np.nan)
    day_list.pop(-1)
    df.insert(len(df.columns),'距上一篇的天数',value=day_list)

    fields = [df.xs('总阅读人数', axis=1), df.xs('初次打开阅读人数', axis=1), df.xs('分享次数', axis=1), df.xs('每日增粉人数', axis=1),
              df.xs('粉丝数', axis=1)]
    to_percent = lambda x: (x * 100).round(1)
    expressions = [('初次打开率', lambda f: f[1] / f[4]), ('分享率', lambda f: f[2] / f[0]), ('分享拉粉率', lambda f: f[3] / f[2]),
                   ('增粉速率', lambda f: f[3] / f[4]), ( '阅读涨粉率', lambda f: f[3] / f[0]),
                   ('传播涨粉率', lambda f: f[3] / (f[0] - f[1])), ('二次传播率', lambda f: (f[0] - f[1]) / f[0])]
    old_field_count = len(df.columns)-2
    # 计算各字段的值，处理为percent后，依次插入datagrame中
    for i in enumerate(expressions, start=old_field_count):
        df.insert(i[0], i[1][0], (i[1][1](fields)).apply(to_percent))
    df.set_index('距下一篇的天数').dropna().groupby(level =0).mean().T[5:12].plot(kind='barh', figsize=(16, 9))
    df.set_index('距上一篇的天数').dropna().groupby(level =0).mean().T[5:12].plot(kind='barh', figsize=(16, 9))
    groupby=df.groupby(lambda x:x[:2])
    df=groupby.mean()
    df.insert(5,'连载篇数',groupby.count()[['标题']])
    df.set_index('连载篇数').groupby(level=0).mean().T[5:12].plot(kind='barh', figsize=(16, 9))
    # df.dropna().set_index('距下一篇的天数')
    # df.plot(kind='barh', figsize=(16, 9))
    #
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.show()