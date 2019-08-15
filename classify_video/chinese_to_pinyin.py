# -*- coding: utf-8 -*-
import csv
import pinyin

def to_pinyin(var_str):
    """
    汉字[钓鱼岛是中国的]=>拼音[diaoyudaoshizhongguode]\n
    汉字[我是shui]=>拼音[woshishui]\n
    汉字[AreYou好]=>拼音[AreYouhao]\n
    汉字[None]=>拼音[]\n
    汉字[]=>拼音[]\n
    :param var_str:  str 类型的字符串
    :return: 汉字转小写拼音
    """
    if isinstance(var_str, str):
        if var_str == 'None':
            return ""
        else:
            return pinyin.get(var_str, format='strip', delimiter="")
    else:
        return '类型不对'


def get_chinese():
    chinese_list = []
    with open('/Users/yyinc/Downloads/hero_list1.csv','rU') as hero:
        reader = csv.reader(hero)
        for line in reader:
            chinese_list.append(line[0])
    return chinese_list

def main():
    chinese_list = get_chinese()
    chinese_list.pop(0)
    pinyin_list = []
    for _ in chinese_list:
        # print to_pinyin(_)
        p = to_pinyin(_)
        pinyin_list.append(p)
    # print pinyin_list
    # for i in pinyin_list:
    #     print i
    dictionary = dict(zip(chinese_list,pinyin_list))
    count = 0
    for i in dictionary:
        count += 1
        print '| {0} | {1} | {2} |'.format(i,dictionary[i],count)
        # print '{} = {}'.format(dictionary[i], count)
    # for i in pinyin_list:
    #     count += 1
    #     print '{} = {}'.format(i,count)

    # print count

if __name__ == '__main__':
    # get_chinese()
    main()
    # a = ['a','b','c']
    # b = ['d','e','f']
    # d = dict(zip(a,b))
    # print d