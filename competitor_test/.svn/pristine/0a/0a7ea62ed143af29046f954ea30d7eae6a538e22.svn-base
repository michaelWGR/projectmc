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
    parser.add_argument('file_path')
    args = parser.parse_args()

    file_path = os.path.abspath(args.file_path)
    with open(file_path, 'rb') as file:
        m = md5.new(file.read())
        print m.hexdigest()

if __name__ == '__main__':
    main()
