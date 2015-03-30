# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import sys


import os
import sqlite3
import re
import sys

chatdata = r"resource/小黑的情怀.mht"
db_filename = r'resource/小黑的情怀.db'
schema_filename = r'schema.sql'

# ##############################################################

def insertdata():
    '''
     数据导入数据库,从qq里面导出的数据选 mht格式 (实际就是Html 格式)
     表结构 见schema.sql 里面的 chatdb
    '''

    db_is_new = not os.path.exists(db_filename)
    conn = sqlite3.connect(db_filename)
    if db_is_new:
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
    else:
        print('Database exists, assume schema does, too.')

    print('Inserting data ... ')
    with open(chatdata,encoding='utf-8') as f:
        soup = BeautifulSoup(f.read())
        script = soup.find_all('tr')
        print('待处理数据共:', len(script), '条 .......')

        # #############################################
        # 下面完成数据插入
        # 技能模块：BeautifulSoup 数据解析
        # #############################################
        # 你的主要代码在这里
        date = None
        # conn.execute('DELETE FROM chatdb')
        for i in script:
            try:
                if not i.td.div:
                    date = i.td.string[4:].replace('-', r'/')
                else:
                    speaker = i.td.div.div.string
                    if ')' == speaker[-1]:
                        speaker = re.findall(r'(.*?)\((\d+)\)', speaker)
                    else:
                        speaker = re.findall(r'(.*?)<(.*?)&get;', speaker)
                    s_name = speaker[0][0]
                    s_id = speaker[0][1]
                    time = i.td.div.contents[1]

                    content = ''.join([ttt for ttt in i.td.contents[1].strings])
                    conn.execute('INSERT INTO chatdb (name,usrid,date, time, contents) VALUES(?,?,?,?,?)',
                                 (s_name, s_id, date, time, content))
            except Exception as e:
                pass

        conn.commit()
        print(' ok! ')


def someonechat(usrid=None, name=None):
    '''
      查询到某个id 的所有发言记录，放入一个list 返回
      list 每个元素对应数据库一条记录，改成字典表示, 字典每个关键字命名对应字段名
    '''
    # 你的主要代码在这里
    conn = sqlite3.connect(db_filename)
    if not usrid:
        result = conn.execute('SELECT usrid FROM chatdb WHERE name=? ORDER BY date DESC,time DESC LIMIT 1 ', (name,))
        usrid = result.fetchone()[0]
    print(usrid)
    result = conn.execute('SELECT id,name,date,time,contents FROM chatdb WHERE usrid=?', (usrid,))
    chatlist = [{'id': i[2], 'name': i[1], 'usrid': id, 'date': i[2], 'time': i[3], 'contents': i[4]} for i in
                result.fetchall()]
    return chatlist