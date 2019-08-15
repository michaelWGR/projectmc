# -*- coding:utf-8 -*-
import argparse
import subprocess
import time


def main():
    argparser = argparse.ArgumentParser('list helper')
    argparser.add_argument('app')
    args = argparser.parse_args()
    app_name = args.app
    for i in range(1, 7):
        print "record {} begin".format(i)
        cmd_record = "adb shell screenrecord --bit-rate 16000000 /sdcard/shortvideos/list/{}_android_list_0{" \
                     "}.mp4".format(
            app_name, i).split()
        cmd_swipe = "adb shell input swipe 540 240 540 1920".split()
        p_record = subprocess.Popen(cmd_record)
        time.sleep(1)
        p_swipe = subprocess.Popen(cmd_swipe)
        time.sleep(5)
        p_record.kill()
        print "record {} end".format(i)
    print "finish"

if __name__ == '__main__':
    main()
