# -*- coding: UTF-8 -*-






################################
# 测    试
################################
def main():
    pass


# 导入数据
def t_insertdata():
    import dataio
    dataio.insertdata()


# 查询某人的发言
def t_someonechat():
    import dataio
    id = u'黄师傅'
    chatlist = dataio.someonechat(name=id)
    print(u'总共发言说话次数:', len(chatlist))
    for x in chatlist:
        print(x['contents'])


# 查询某人的发言
def t_pet_phrase():
    import s103
    print(s103.pet_phrase(name=u'W540'))


def t_s104():
    import s104
    print(s104.s104(name=u'木帆船'))


def t_s105():

    import s105
    # s105.insertdata()
    # s105.jieba()
    s105.pandas()


def t_s106():
    import s106

    s106.analyse()


def t_s107():
    import s107

    s107.analyse()


def t_s108():
    import s108

    s108.analyse()


def t_s109():
    import s109

    s109.analyse(name=u'')


def t_s110():
    import s110

    # s110.read_data()
    print(s110.link_in_count('A'))


if __name__ == '__main__':
    # t_insertdata()
    # t_someonechat()
    # t_pet_phrase()
    # t_s104()
    # t_s105()
    # t_s106()
    # t_s107()
    # t_s108()
    # t_s109()
    t_s110()
