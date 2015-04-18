# -*- coding: utf-8 -*-
__author__ = 'sail'
import jieba
import jieba.analyse
import jieba.posseg as posseg
import dataio
from collections import *

db_filename = r'resource/chat.db'


def analyse(usrid=None, name=None):
    with open(r'resource/stopWordList.txt', encoding='utf-8') as f:
        black_list = [i for i in f.read().split('\n')]
    speak_list = dataio.someonechat(usrid, name)
    words = [i for i in jieba.posseg.cut(' '.join([i['contents'] for i in speak_list])) if i.word not in black_list]
    word_dict=defaultdict(list)
    for i in words:
        if i.flag != 'eng':
            i.flag = i.flag[0]
        word_dict[i.flag].append(i.word)
    print(Counter(word_dict['v']).most_common(10))
    print(Counter(word_dict['n']).most_common(10))
    print(Counter(word_dict['a']).most_common(10))