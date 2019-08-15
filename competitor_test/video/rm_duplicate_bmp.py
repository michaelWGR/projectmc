# /usr/bin/env python
# -*- coding:utf-8 -*-

import md5
import os
import argparse


def getmd5(filename):
    file = open(filename, 'rb').read()
    m = md5.new(file)
    return m.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path')
    args = parser.parse_args()

    dir_path = os.path.normpath(args.dir_path)

    md5_std = None
    count = 0
    files = os.listdir(args.dir_path)
    files.sort()
    for file in files:
        if file.lower().endswith('.bmp'):
            path = os.path.join(dir_path, file)
            md5 = getmd5(path)
            if md5 == md5_std:
                print('remove %s, md5: %s' % (file, md5))
                count += 1
                os.remove(path)
            else:
                md5_std = md5
                print('%s is a new file, md5_std changed: %s' %
                      (file, md5_std))
    print('total removed: %d' % count)


if __name__ == '__main__':
    main()
