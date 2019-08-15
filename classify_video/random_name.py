# -*- coding: utf-8 -*-
import os
import random


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

def new_file_path(ocr,old_path,random_string):
    ocr_map = {
        '1': 'jdqs_righttop_',
        '3': 'jdqs_end_',
        '4': 'jdqs_',
        '5': 'hyxd_lefttop_',
        '6': 'cjzc_lefttop_',
        '7': 'cjcj_lefttop_',
        '9': 'wzry_',
    }

    dirs, files = os.path.split(old_path)
    fname, fextension = os.path.splitext(files)
    new_name = ''

    if ocr in ['1', '3', '5', '6', '7']:
        new_name = ocr_map[ocr]+random_string

    elif ocr in ['4','9']:
        up_dirs,up_files = os.path.split(dirs)
        second_name = ''
        for letter in up_files.lower():
            if letter in 'abcdefghijklmnopqrstuvwxyz1234567890':
                second_name = second_name + letter

        new_name = '{}{}_{}'.format(ocr_map[ocr],second_name,random_string)
    new_path = old_path.replace(fname,new_name)

    return new_path

def random_string():
    rangeLetter = 'abcdefghijklmnopqrstuvwxyz1234567890'
    random_letter = ''
    for _ in range(10):
        random_letter = random_letter+random.choice(rangeLetter)
    return random_letter

def check_duplication(check_dir,check_string):
    file_list = readDir(check_dir)
    for f in file_list:
        if check_string in f:
            return True

    return False

def main():

    top_dirs = '/Volumes/I/video'
    video_dirs = '/Volumes/I/video/3'
    ocr_group = '3'

    video_list = readDir(video_dirs)
    for path in video_list:

        random_str = random_string()
        while check_duplication(top_dirs,random_str):
            random_str = random_string()

        new_path = new_file_path(ocr_group,path,random_str)
        print new_path
        os.rename(path,new_path)


    print 'finished!!'

if __name__ == '__main__':
    main()