# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import re
import time
import subprocess

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

#获取元素的坐标
def get_coord(str):
    tree = ET.ElementTree(file=get_xml())
    for elem in tree.iter(tag='node'):
        d=elem.attrib
        if d.has_key("resource-id"):
            if d.get("resource-id")==str:
                bou=d.get('bounds')
                pattern=re.compile(r'\[(\d*),(\d*)\]\[(\d*),(\d*)\]')
                result=re.match(pattern,bou)
                x=(int(result.group(1))+int(result.group(3)))/2
                y=(int(result.group(2))+int(result.group(4)))/2
                return x,y

def judge_video(text):
    tree = ET.ElementTree(file=get_xml())
    for elem in tree.iter(tag="node"):
        d = elem.attrib
        if d.get("text") == text:
            return True
        else:
            return False
def get_coord_text(text):
    # while True:
        tree = ET.ElementTree(file=get_xml())
        for elem in tree.iter(tag='node'):
            d = elem.attrib
            if d.has_key("text"):
                if d.get("text") == text:
                    bou = d.get('bounds')
                    pattern = re.compile(r'\[(\d*),(\d*)\]\[(\d*),(\d*)\]')
                    result = re.match(pattern, bou)
                    x = (int(result.group(1)) + int(result.group(3))) / 2
                    y = (int(result.group(2)) + int(result.group(4))) / 2
                    return x, y
        # while get_coord_text(text) == None:
        #     cmd_swipe = "adb shell input swipe 541 1775 541 1242".split()
        #     p_swipe = subprocess.Popen(cmd_swipe)
        #     p_swipe.communicate()
                # else:
                #     cmd_swipe = "adb shell input swipe 541 1775 541 1242".split()
                #     p_swipe = subprocess.Popen(cmd_swipe)
                #     p_swipe.communicate()
                #     # tree = ET.ElementTree(file=get_xml())
                #     break

# def connectDevice():
#     '''''检查设备是否连接成功，如果成功返回True，否则返回False'''
#     try:
#         '''''获取设备列表信息，并用"\r\n"拆分'''
#         deviceInfo= subprocess.check_output('adb devices').split("\r\n")
#         '''''如果没有链接设备或者设备读取失败，第二个元素为空'''
#         if deviceInfo[1]=='':
#             return False
#         else:
#             return True
#     except Exception,e:
#         print "Device Connect Fail:",e


#模拟点击手机屏幕
def tap(str):
    cont = str.decode("utf-8")
    x,y=get_coord(cont)
    cmd_tap = "adb shell input tap {} {}".format(x,y).split()
    p_tap = subprocess.Popen(cmd_tap)
    print x,y
    p_tap.communicate()

def tap_text(text):
    cont_text = text.decode("utf-8")
    x, y = get_coord_text(cont_text)
    cmd_tap = "adb shell input tap {} {}".format(x, y).split()
    p_tap = subprocess.Popen(cmd_tap)
    print x, y
    p_tap.communicate()

def main():
    # id_record = "video.like:id/btn_record"
    # tap(id_record)
    #
    # id_entrance = "video.like:id/ll_entrance_album"
    # tap(id_entrance)

    text_video = "0:15"
    tap_text(text_video)


if __name__ == "__main__":
    main()
