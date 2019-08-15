# -*- coding: utf-8 -*-

import os
import random
import shutil

video_files = 'test1'


def readDir(dir_path):
    all_files = []
    if dir_path[-1] == os.sep:
        print u'文件夹路径末尾不能有{}'.format(os.sep)
        return

    if os.path.isdir(dir_path):
        filelist = os.listdir(dir_path)

        for f in filelist:
            f = os.path.join(dir_path,f)

            if os.path.isdir(f):
                sub_files = readDir(f)
                all_files = sub_files + all_files
            elif f.endswith('.mp4') or f.endswith('.flv') or f.endswith('.mkv'):
                all_files.append(f)

        return all_files
    else:
        return 'Erro no dir'


def get_video_path():
    path_list = []
    first_dirs = os.listdir(video_files)
    for i in first_dirs:
        first_path = os.path.join(video_files, i)

        if os.path.isfile(first_path) and (i != '.DS_Store') and (i.endswith('.mp4') or i.endswith('.flv') or i.endswith('.mkv')):
            path_list.append(os.path.join(video_files,i))
            continue

        if os.path.isdir(first_path):
            second_dirs = os.listdir(first_path)

            for j in second_dirs:
                second_path = os.path.join(first_path, j)

                if os.path.isfile(second_path) and (j != '.DS_Store') and (j.endswith('.mp4') or j.endswith('.flv') or j.endswith('.mkv')):
                    path_list.append(os.path.join(first_path,j))
                    continue

                if os.path.isdir(second_path):
                    third_dirs = os.listdir(second_path)

                    for k in third_dirs:
                        third_path = os.path.join(second_path, k)
                        if os.path.isfile(third_path) and (k != '.DS_Store') and (k.endswith('.mp4') or k.endswith('.flv') or k.endswith('.mkv')):
                            path_list.append(third_path)
                            continue
    return path_list
def test():
    # item = 'UP-we.sldfjRIU09'
    # print item.lower()
    # second_name = ''
    # for letter in item.lower():
    #     if letter in 'abcdefghijklmnopqrstuvwxyz1234567890':
    #         second_name = second_name+letter
    #
    # print second_name
    # print item.replace('UP','dsj')
    old = '/Users/yyinc/Documents/guirong/projectmc/classify_video/test1/1/wzry_1_1wemnrbpw3'
    new = '/Users/yyinc/Documents/guirong/projectmc/classify_video/test1/9/test.mp4'
    shutil.move(old,new)

if __name__ == '__main__':
    # readDir(video_files)
    test()