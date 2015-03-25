# -*- coding: UTF-8 -*-

import dataio
import s103

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
    print(s103.pet_phrase(name=u'黄师傅'))


def test():
    result=[]
    for i in range(4):
        def t(num):
            return num*i
        result.append(t)
    return result

if __name__ == '__main__':
    # t_insertdata()
    # t_someonechat()
    t_pet_phrase()