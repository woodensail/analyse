__author__ = 'sail'
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import sys

import os
import sqlite3
import re
import sys

chatdata = r"resource/weibodata201406.xml"
db_filename = r'resource/weibo.db'
schema = '''create table chatdb (
    id           integer primary key autoincrement not null,
    name         text,
    usrid        text,
    weiboid        text,
    time         datetime,
    contents     text,
    forward int,
    comment int
);'''


def insertdata():
    '''
     数据导入数据库,从qq里面导出的数据选 mht格式 (实际就是Html 格式)
     表结构 见schema.sql 里面的 chatdb
    '''

    db_is_new = not os.path.exists(db_filename)
    conn = sqlite3.connect(db_filename)
    if db_is_new:
        print('Creating schema')
        conn.executescript(schema)
    else:
        print('Database exists, assume schema does, too.')

    print('Inserting data ... ')
    with open(chatdata, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read())
        script = soup.find_all('weibo')
        print('待处理数据共:', len(script), '条 .......')

        # #############################################
        # 下面完成数据插入
        # 技能模块：BeautifulSoup 数据解析
        # #############################################
        # 你的主要代码在这里
        date = None
        conn.execute('DELETE FROM chatdb')
        for i in script:
            try:
                name = i.contents[0].string
                usrid = i.contents[1].string
                weiboid = i.contents[3].string
                time = i.contents[2].string.replace('-', r'/')
                contents = i.contents[4].string
                forward = i.contents[5].string
                comment = i.contents[6].string
                conn.execute('INSERT INTO chatdb (name,usrid,weiboid, time, contents,forward,comment) VALUES(?,?,?,?,?,?,?)',
                             (name, usrid, weiboid, time, contents,forward,comment))
            except Exception as e:
                pass

        conn.commit()
        print(' ok! ')

def jieba():
    import jieba.analyse
    conn = sqlite3.connect(db_filename)
    result = '\n'.join([i[0] for i in conn.execute('SELECT contents FROM chatdb')])
    print(jieba.analyse.extract_tags(result, 10))
    print(jieba.analyse.textrank(result,10))

def pandas():
    import pandas as pd
    import matplotlib.pyplot as plt
    conn = sqlite3.connect(db_filename)

    df =pd.read_sql('SELECT * FROM chatdb',conn,parse_dates=['time'],index_col=['time'])
    df.groupby(lambda x:x.hour).count()[['contents']].plot()
    plt.xlim(0,23)
    df.groupby(lambda x:x.dayofweek).count()[['contents']].rename({0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}).plot()
    plt.xlim(0,6)
    plt.show()