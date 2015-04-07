__author__ = 'sail'
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


def analyse():
    df = pd.ExcelFile(r"resource/wxgzhdata.xlsx").parse(u"3月")
    prev = []
    articles={}
    titles=[]
    for i in df.as_matrix():
        prev = [i[j]+prev[j-1] for j in range(1,5)] if prev else [i[j] for j in range(1,5)]
        prev.append(i[6])
        if not isinstance(i[6],float):
            title=i[6][:2]
            if title not in titles:
                titles.append(title)
                articles[title]=prev
                prev=None
            else:
                for i in range(4):
                    articles[title][i]+=prev[i]
                for i in range(len(articles[title][4])):
                    if articles[title][4][i]!=prev[4][i]:
                        break
                else:
                    i+=1
                articles[title][4]=prev[4][:i]
                prev=None
    articles={i[4]:[i[0],i[1],i[2],i[3]] for i in articles.values()}
    df2=pd.DataFrame(articles).rename({0:'总阅读',1:'初次打开阅读',2:'分享次数',3:'增粉数'})
    df2.plot(kind='bar')
    df2.T.plot(kind='barh')
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
    plt.show()
    print(df2)