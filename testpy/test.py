# -*- coding:utf-8 -*-

import argparse
import os
import re
import csv
import random
import subprocess
import time
import sys
import requests
import webbrowser
import json
# import psutil
import threading
import signal
import pickle
import platform
# import pinyin
# from pinyin._compat import u
from httprunner.api import HttpRunner
from httprunner.utils import get_os_environ

def main():
    print(sys.getdefaultencoding())
    a = '你好'
    print(type(a.encode().decode('utf-8').encode('utf-8')))


if __name__ == '__main__':
    main()
