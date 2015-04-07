# -*- coding: UTF-8 -*-

import dataio
import s103
import s104
import s105


################################
# 测    试
################################
def main():
    pass


# 导入数据
def t_insertdata():
    dataio.insertdata()


# 查询某人的发言
def t_someonechat():
    id = u'黄师傅'
    chatlist = dataio.someonechat(name=id)
    print(u'总共发言说话次数:', len(chatlist))
    for x in chatlist:
        print(x['contents'])


# 查询某人的发言
def t_pet_phrase():
    print(s103.pet_phrase(name=u'W540'))


def t_s104():
    print(s104.s104(name=u'木帆船'))


def t_s105():
    # s105.insertdata()
    # s105.jieba()
    s105.pandas()


def t_s106():
    import s106
    s106.analyse()


if __name__ == '__main__':
    # t_insertdata()
    # t_someonechat()
    # t_pet_phrase()
    # t_s104()
    # t_s105()
    t_s106()