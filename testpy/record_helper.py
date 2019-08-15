# -*- coding:utf-8 -*-
import argparse
import os
import subprocess
import time

mobile_directory = "/sdcard/yypm"


def check_directory():
    cmd_find = "adb shell find {}".format(mobile_directory).split()
    cmd_mkdir = "adb shell mkdir {}".format(mobile_directory).split()

    output = subprocess.check_output(cmd_find)

    if "No such file or directory" in output:
        print ("Making dir {}".format(mobile_directory))
        p = subprocess.Popen(cmd_mkdir)
        p.communicate()


def record(name, duration):
    print ("Record begin.")
    file_name = "{}/{}.mp4".format(mobile_directory, name)
    cmd_record = "adb shell screenrecord --bit-rate 16000000 {}".format(file_name).split()

    p_record = subprocess.Popen(cmd_record)
    if duration > 0:
        print("Record duration: {}s".format(duration))
        time.sleep(duration)
    else:
        raw_input("press enter to quit record.")
    # os.killpg(os.getpgid(p_record.pid), signal.SIGTERM)
    p_record.terminate()
    print ("Record finish.")
    return file_name


def pull_and_del_file(directory, file_name):
    # 如果在结束进程马上就拉视频有问题，估计是手机内部没有处理好视频
    time.sleep(1)

    cmd_pull = "adb pull {} {}".format(file_name, directory).split()
    cmd_del = "adb shell rm {}".format(file_name).split()

    p_pull = subprocess.Popen(cmd_pull)
    p_pull.communicate()

    p_del = subprocess.Popen(cmd_del)
    p_del.communicate()


def main():
    argparser = argparse.ArgumentParser('loadtime helper')
    argparser.add_argument('directory', help="电脑保存的目录")
    argparser.add_argument('name', help="视频的名字，请不要增加 mp4 后缀，e.g : yy_android_start_01")
    argparser.add_argument('-d', '--duration', default=0, help='采集时间', type=int)
    args = argparser.parse_args()
    directory = args.directory
    name = args.name
    duration = args.duration

    if not os.path.exists(directory):
        os.mkdir(directory)

    # Check mobile directory
    check_directory()

    # Record
    file_name = record(name, duration)

    # Pull video and del the file in the mobile
    pull_and_del_file(directory, file_name)


if __name__ == '__main__':
    main()
