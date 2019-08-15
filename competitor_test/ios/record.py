# -*- coding:utf-8 -*-
import os


def main():
    for i in range(0, 6):
        print i
        os.popen("osascript quicktime.scpt")
        print str(i) + 'finish'


if __name__ == '__main__':
    main()
