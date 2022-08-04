# -*- coding: utf-8 -*-



def reset():
    with open('/Users/michael/Downloads/lovemeet_20201215.xlog', 'rb') as f:
        read = f.read().decode('utf8', 'ignore')
        print(read)


if __name__ == '__main__':
    reset()