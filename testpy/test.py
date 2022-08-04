# -*- coding:utf-8 -*-

import argparse
import os
import re
import csv
import random
import subprocess
import time
import sys
# import requests
import webbrowser
import json
# import psutil
import threading
import signal
import pickle
import platform
# import pinyin
# from pinyin._compat import u
# from httprunner.api import HttpRunner
# from httprunner.utils import get_os_environ


def main():
    # print(sys.getdefaultencoding())
    # a = '你好'
    # print(type(a.encode().decode('utf-8').encode('utf-8')))
    earning = [2.19, 3.08, 2.96, 2.90, 2.70, 2.54, 2.25, 1.88, 1.83, 1.59]
    earning_rate = [-28.91, 4.16, 1.93, 7.44, 6.50, 12.76, 19.55, 2.62, 15.27, 105.56]
    # print(len(earning))
    per_earning = sum(earning)/len(earning)
    per_earning_rate = sum(earning_rate)/len(earning_rate)
    value = per_earning*(8.5+per_earning_rate*2)
    # print(per_earning_rate*2)
    # print(per_earning)
    print(value)
    pay = per_earning*20*2/3
    print(pay)
    proper = (5111.58-4628.03)/116.8
    print(proper)
    print('#######')

    su_earn = [1.07, 1.44, 0.45, 0.08, 0.12, 0.12, 0.05, 0.37, 0.69, 0.57]
    su_e_rate = [-25.69, 220, 462.50, -33.33, 0, 140, -86.49, -46.3, 20.88, 32.56]
    per_su_earn = sum(su_earn)/len(su_earn)
    per_su_e_rate = sum(su_e_rate)/len(su_earn)
    value = per_su_earn*(8.5+per_su_e_rate*2)
    print(value)
    pay = per_su_earn*20*2/3
    print(pay)
    print('####')

    hua_earn = [1.61, 1.29, 1.22, 1.5, 2.53, 1.74, 1.32, 1.08, 0.88, 0.73]
    hua_e_rate = [24.81, 5.74, -18.67, -40.71, 45.4, 31.82, 22.22, 22.73, 20.55, -16.09]
    per_hua_earn = sum(hua_earn)/len(hua_earn)
    per_hua_e_rate = sum(hua_e_rate)/len(hua_e_rate)
    hua_value = per_hua_earn*(8.5+per_hua_e_rate*2)
    print(hua_value)
    hua_pay = per_hua_earn*20*2/3
    print(hua_pay)


def write_file():
    with open('test.yml', 'a') as f:
        f.write('# 哈哈哈哈哈\n')
        f.write('# 哈哈哈哈哈\n')


if __name__ == '__main__':
    # main()
    # write_file()
    a = 78890
    b = 67490
    print(abs(b-a))
    print(19*0.2*3000)