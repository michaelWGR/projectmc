# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import time
import subprocess
import sys
import argparse


__author__ = 'Michael'


#获取元素的坐标
def get_coord(str):
    tree = ET.ElementTree(file=get_xml())
    for elem in tree.iter(tag='node'):
        d=elem.attrib
        if d.has_key('content-desc'):
            if d.get('content-desc')==str:
                bou=d.get('bounds')
                pattern=re.compile(r'\[(\d*),(\d*)\]\[(\d*),(\d*)\]')
                result=re.match(pattern,bou)
                x=(int(result.group(1))+int(result.group(3)))/2
                y=(int(result.group(2))+int(result.group(4)))/2
                # return result.group(1),result.group(2)
                return x,y
# 判断手机是否连接成功
def connectDevice():
    cmd_device = 'adb devices'.split()
    p_device = subprocess.Popen(cmd_device, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_device.wait()
    deviceInfo = p_device.stdout.readlines()
    if deviceInfo[1] == '\n':
        print u'设备未连接，请重新连接设备'
        sys.exit()
    else:
        return True

#获取手机xml文件地址
def get_xml():
    #begin = time.time()
    cmd_dump = "adb shell uiautomator dump /sdcard/andro.xml".split()
    p_dump = subprocess.Popen(cmd_dump)
    p_dump.communicate()
    #after = time.time()
    #print("Get xml duration1 : {}s".format(after - begin))
    cmd_pull = "adb pull /sdcard/andro.xml".split()
    p_pull = subprocess.Popen(cmd_pull)
    p_pull.communicate()
    #after = time.time()
    #print("Get xml duration2 : {}s".format(after - begin))
    return "andro.xml"

#模拟点击手机屏幕
def tap(str):
    cont = str.decode("utf-8")
    x,y=get_coord(cont)
    cmd_tap = "adb shell input tap {} {}".format(x,y).split()
    p_tap = subprocess.Popen(cmd_tap)
    p_tap.communicate()

# 获取当前应用的包名
def get_package():
    cmd_package = 'adb shell dumpsys activity | grep mFocusedActivity'.split()
    p_package = subprocess.Popen(cmd_package, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_package.wait()
    p_out = p_package.stdout.readlines()
    p_package.stdout.close()
    for item in p_out:
        pattern_package = re.compile(r'.*u0\s+([^\s]+)/')
        package_name = pattern_package.match(item).group(1)
        return package_name

def main():
    app_map = {
        'dyin': '抖音短视频',
        'ks': '快手',
        'like': 'LIKE短视频',
        'soda': '燥点小视频',
    }

    parser = argparse.ArgumentParser(description='app启动耗时录制')
    parser.add_argument('--app',dest= 'app',help= '需要录制的app简称')
    parser.add_argument('-c','--count',dest='count',type=int, default=1, help= '录制的次数')
    args = parser.parse_args()

    param_app = args.app
    # if args.count is not None:
    param_count = args.count
    # else:
    #     param_count = 1

    connectDevice()
    for i in range(param_count):
        step1 = app_map[param_app]
        tap(step1)
        time.sleep(5)
        package_name = get_package()
        cmd = 'adb shell am force-stop {}'.format(package_name).split()
        p_stop = subprocess.Popen(cmd)
        p_stop.wait()

if __name__ == "__main__":
    main()