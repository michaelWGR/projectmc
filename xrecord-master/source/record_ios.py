# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import re
import argparse
import signal

def get_command_dir():
    source_dir = sys.path[0]
    root_dir = os.path.split(source_dir)[0]
    command_dir = os.path.join(root_dir,'bin/xrecord')
    return command_dir

def get_device_id():
    command_dir = get_command_dir()
    cmd = '{} --quicktime --list'.format(command_dir).split()
    p_device = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_out = p_device.stdout.readlines()
    p_device.stdout.close()
    for item in p_out:
        try:
            pattern = re.compile(r'[^A-Z]')
            re.match(pattern,item).group()
            device_id = item.split(':')[0].strip()
            return device_id
        except AttributeError:
            continue
    print u'识别不到iphone手机'
    sys.exit()

def get_video_dir(video_name):
    source_dir = sys.path[0]
    root_dir = os.path.split(source_dir)[0]
    data_dir = os.path.join(root_dir,'data')
    isExit = os.path.exists(data_dir)
    if not isExit:
        cmd = 'mkdir -p {}'.format(data_dir).split()
        p_mkdir = subprocess.Popen(cmd)
        p_mkdir.wait()
    video_dir = os.path.join(data_dir,video_name)
    return video_dir

def record_video(device_id,video_dir):
    command_dir = get_command_dir()
    cmd = '{} --quicktime --id={} --out={} --force'.format(command_dir,device_id,video_dir).split()
    p_record = subprocess.Popen(cmd,stdout=subprocess.PIPE)

    while True:
        isexist = os.path.exists(video_dir)
        if isexist:
            print u'开始录制'
            p_record.wait()
            break

def quit(num,stack):
    print u'结束录制'
    sys.exit()

def main():
    parser = argparse.ArgumentParser(description='ios录制视频')
    parser.add_argument('--output',dest= 'output',help= '视频输出路径')
    parser.add_argument(dest='video_name', help= '视频名称')
    args = parser.parse_args()

    param_output = args.output
    param_video_name = args.video_name

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    device_id = get_device_id()

    if param_output is None:
        video_dir = get_video_dir(param_video_name)
    else:
        video_dir = get_video_dir(param_output)

    if os.path.exists(video_dir):
        os.remove(video_dir)

    print u'提示：请配置好环境'
    
    record_video(device_id,video_dir)


if __name__ == '__main__':
    main()