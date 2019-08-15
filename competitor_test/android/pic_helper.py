# -*- coding:utf-8 -*-
import argparse
import subprocess
import time


def main():
    cmd_swipe = "adb shell input swipe 540 1460 540 240 150".split()
    argparser = argparse.ArgumentParser('list helper')
    argparser.add_argument('app')
    args = argparser.parse_args()
    app_name = args.app
    for i in range(1, 7):
        print "record {} begin".format(i)
        cmd_record = "adb shell screenrecord --bit-rate 16000000 /sdcard/shortvideos/sspic/{}_android_sspic_0{" \
                     "}.mp4".format(
            app_name, i).split()
        time.sleep(1)
        p_record = subprocess.Popen(cmd_record)
        for j in range(0, 10):
            p_swipe = subprocess.Popen(cmd_swipe)
            time.sleep(0.5)
            p_swipe.wait()
        p_record.kill()
        print "record {} end".format(i)
    print "finish"

if __name__ == '__main__':
    main()
