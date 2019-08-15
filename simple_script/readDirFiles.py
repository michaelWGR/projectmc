# -*- coding: utf-8 -*-
# 功能：读取传入的目录下所有的文件（包括该目录下的所有子目录）的绝对路径，并以列表形式返回所有文件的绝对路径
# 要求传入的路径参数最后不能有斜杠,目的是为了递归时格式统一

import os


def readDir(dir_path, layer=0):             # layer为设置的层级，默认为0，遍历所有，层级为1，只遍历第一层的文件
    all_files = []

    if dir_path[-1] == os.sep:
        print u'文件夹路径末尾不能有{}'.format(os.sep)
        return
    if layer == 0:
        if os.path.isdir(dir_path):
            filelist = os.listdir(dir_path)

            for f in filelist:
                f = os.path.join(dir_path,f)

                if os.path.isdir(f):
                    sub_files = readDir(f)
                    all_files = sub_files + all_files
                else:
                    all_files.append(f)

            return all_files
        else:
            return 'Erro no dir'
    else:
        if os.path.isdir(dir_path):
            filelist = os.listdir(dir_path)

            for f in filelist:
                f = os.path.join(dir_path,f)

                if os.path.isdir(f):
                    if layer > 1:
                        layer -= 1
                        sub_files = readDir(f, layer)
                        all_files = sub_files + all_files
                else:
                    all_files.append(f)

            return all_files
        else:
            return 'Erro no dir'


if __name__ == '__main__':

    dirs = '/Users/michael/Documents/guirong/projectmc/classify_video/test1/1'
    files_list = readDir(dirs, 3)
    for f in files_list:
        print f


    # layer = 2
    # for i in range(1, layer):
    #     print i
