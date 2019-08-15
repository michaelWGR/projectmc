# -*- coding: utf-8 -*-
#获取本机ip4
#判断一个进程是否存在
#带上本机ip，发送http请求给web服务器
#request
#打印log

import socket
import requests
import subprocess
import logging
import time
import psutil
import platform

def check_system():
    sysstr = platform.system()
    if sysstr == "Darwin":
        return ""
    if sysstr == "Windows":
        return ".exe"
#获取本机电脑名
def get_ip():
    myname = socket.getfqdn(socket.gethostname())
    #获取本机ip
    myaddr = socket.gethostbyname(myname)
    return myaddr

def check_process(process_name):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myapp.log',
                        filemode='a')
    iter = psutil.process_iter()
    for process in iter:
        if process.name() == process_name+check_system():
            logging.info("alive=1")
            return 1
    logging.info("alive=0")
    return 0

def check_exsit(process_name):
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a')
    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)
    p_list = subprocess.check_output(cmd)
    #print p_list
    for line in p_list.splitlines():
        if process_name in line:
            logging.info('alive=1')
            return 1
    logging.info('alive=0')
    return 0

def post_ip():
    url = "http://www.baidu.com"
    my_data = {
        "ip":get_ip(),
        "alive":check_process("QQ")
    }
    r = requests.post(url,data = my_data)

def main():
    while True:
        print get_ip()
        print check_process("QQ")
        post_ip()
        second = 2
        time.sleep(second)

if __name__ == "__main__":
    main()