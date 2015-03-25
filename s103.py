# -*- coding: utf-8 -*-
__author__ = 'sail'
import jieba
import jieba.posseg as posseg
import time
import sqlite3
import dataio
db_filename = r'resource/chat.db'


def pet_phrase(usrid=None, name=None):
    with open(r'resource/stopWordList.txt',encoding='utf-8') as f:
        black_list=[i for i in f.read().split('\n')]
    print(black_list)
    speak_list=dataio.someonechat(usrid,name)
    rate={}
    for sentence in speak_list:
        for word in posseg.cut(sentence['contents']):
            s=word.word
            if rate.get(s):
                rate[s]+=1
            elif s not in black_list:
                rate[s]=1
    return sorted(rate.items(),key=lambda x:x[1],reverse=True)[:10]
    # words_list=[[for j in posseg.cut(i)] for i in speak_list]
