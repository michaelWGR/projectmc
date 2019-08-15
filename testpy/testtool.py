# -*- coding:utf-8 -*-

import os

# 返回两个文件夹的名称（路径暂时写死）
def filename(basepath):
    if os.path.isdir(basepath):
        rootlist = os.listdir(basepath)  # 根目录
        dirlist = []  # 文件夹列表

        for i in rootlist:
            i = os.path.join(basepath, i)
            if os.path.isdir(i):  # 判断是否为文件夹
                dirlist.append(i)
        return dirlist

# 比较文件夹下文件是否相同
def repare_filename(dirname):
    list_a = os.listdir(dirname[0])  # a文件夹下的文件
    list_b = os.listdir(dirname[1])  # b文件夹下的文件

    a = [x for x in list_a if x in list_b]  # 两个列表都存在
    b = [y for y in (list_a + list_b) if y not in a]  # 两个列表中的不同元素

    # c = [x for x in list_a if x not in list_b]  # 在list1列表中而不在list2列表中
    c = []
    for x in list_a:
        if x not in list_b:
            c.append(x)
    d = [y for y in list_b if y not in list_a]  # 在list2列表中而不在list1列表中

    for data in c:

        msg.append(u"文件夹 {} 中多了文件 {} ".format(dirname[0].decode('gbk'), data.decode('gbk')))
    for data in d:
        msg.append(u"文件夹 {} 中多了文件 {}".format(dirname[1].decode('gbk'), data.decode('gbk')))

    return a

# 比较文件内容是否相同
def repare_file(dirname, a):
    file_a = dirname[0]
    file_b = dirname[1]
    for name in a:
        file_name1 = basepath + '\\' + file_a + '\\' + name
        file_name2 = basepath + '\\' + file_b + '\\' + name

        f1 = open(file_name1)
        f2 = open(file_name2)

        count = 1
        for line1 in f1:
            line2 = f2.readline()
            if (line1 != line2):
                msg.append("%s第%d行不一样" % (name, count))  # 多一个换行符也会提示不一样...
            count += 1

        f1.close()
        f2.close()

    for s in msg:
        print s

    return msg

if __name__ == '__main__':
    basepath = r'C:\Users\wangguirong\Desktop\test'
    msg = []

    dirname = filename(basepath)
    # print(dirname)
    a = repare_filename(dirname)  # 单独输出a中的中文元素会乱码，需要.decode('gb18030')
    repare_file(dirname, a)