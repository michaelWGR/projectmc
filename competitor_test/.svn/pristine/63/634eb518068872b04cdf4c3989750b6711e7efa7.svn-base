# /usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess

'''
    循环调用 num_produce.py 生成指定数量的数字图片
'''


def main():
    for i in range(7571, 7807):
        subprocess.call(['python', 'num_produce.py',
                         '--zfill', '4', str(i), str(10)])


if __name__ == '__main__':
    main()
