# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import time
import subprocess
import sys
import argparse
import os
import signal

__author__ = 'Michael'

current_dir = sys.path[0]

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
        print u'设备未连接，请重新连接android设备'
        sys.exit()
    else:
        return True

#获取手机xml文件地址
def get_xml():
    cmd_dump = "adb shell uiautomator dump /sdcard/android.xml".split()
    p_dump = subprocess.Popen(cmd_dump)
    p_dump.communicate()

    current_dir = sys.path[0]
    cmd_pull = "adb pull /sdcard/android.xml {}".format(current_dir).split()
    p_pull = subprocess.Popen(cmd_pull)
    p_pull.communicate()

    xml_path = os.path.join(current_dir,'android.xml')
    return xml_path

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

#运行ios录制脚本
def record_by_script(video_name):
    scrip_path = os.path.join(current_dir, 'record_ios.py')
    cmd_record = 'python {} {}'.format(scrip_path,video_name).split()
    p = subprocess.Popen(cmd_record,stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=os.setsid)
    out = p.stdout.readline()
    print out.strip()
    if out.strip() != '开始录制':

        print u'识别不到iphone手机'

        sys.exit()
    print 'success'
    return out,p.pid

#通过输入的视频名获取要录制的app名字
def get_app(video_name):
    app_list = ['dyin','ks','like','soda']
    for i in app_list:
        app = re.search(i,video_name)
        if app is not None:
            return app.group()

    print u'视频命名错误'
    sys.exit()

#改变视频的命名
def rename_video(video_name,count):
    name = os.path.splitext(video_name)[0]
    old_count = name.split('_')[3]
    new_count = int(old_count)+int(count)
    num = str(new_count).zfill(2)
    new_video_name = video_name.replace(old_count,num,1)
    return new_video_name

#终止程序，用于signal
def quit(num,stack):
    print u'程序终止'
    sys.exit()

def main():

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    app_map = {
        'dyin': '抖音短视频',
        'ks': '快手',
        'like': 'LIKE短视频',
        'soda': '燥点小视频',
    }

    parser = argparse.ArgumentParser(description='app启动耗时录制')
    parser.add_argument(dest= 'video_name',help= '需要录制的视频名称')
    parser.add_argument('-c','--count',dest='count',type=int, default=1, help= '录制的次数')
    args = parser.parse_args()

    param_video_name = args.video_name
    param_count = args.count

    connectDevice()

    for i in range(param_count):
        app = get_app(param_video_name)

        video_name = rename_video(param_video_name,i)
        print video_name
        start_signal, xrecord_pid = record_by_script(video_name)
        # print start_signal
        try:
            step1 = app_map[app]
            print step1
            tap(step1)
            time.sleep(5)

            os.killpg(xrecord_pid, signal.SIGTERM)

            package_name = get_package()
            cmd = 'adb shell am force-stop {}'.format(package_name).split()
            p_stop = subprocess.Popen(cmd)
            p_stop.wait()
        except:
            print u'程序终止'
            os.killpg(xrecord_pid, signal.SIGTERM)
            break

if __name__ == "__main__":
    main()
    # video_name = '/Users/yyinc/Documents/guirong/projectmc/xrecord-master/data/opr11dyin_android_start_01.mp4'
    # record_by_script(video_name)