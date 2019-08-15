# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
import argparse

defulat_adb_tool_path = ''


def collect_msg(arg_collect_time, arg_log_path, arg_device_id):
    # 根据应用的包名称 获取CPU以及内存占用
    utilization_arg_1 = ""
    utilization_arg_2 = ""
    gpu_frequency = ""
    load = ""

    load_cmd = [os.path.join(defulat_adb_tool_path, "adb"), "-s", arg_device_id, "shell", "cat", "/sys/class/kgsl/kgsl-3d0/gpubusy"]
    frequency_cmd = [os.path.join(defulat_adb_tool_path, "adb"), "-s", arg_device_id, "shell", "cat", "/sys/class/kgsl/kgsl-3d0/gpuclk"]
    while 1:
        # 获取GPU使用情况
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        child = subprocess.Popen(load_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=defulat_adb_tool_path)
        child.wait()
        child_out = child.stdout.readlines()
        child.stdout.close()
        arg = child_out[0]
        location = child_out[0].find('\r')
        arg_list = arg[0:location].strip().split(" ")
        size = len(arg_list)
        utilization_arg_1 = arg_list[0]
        utilization_arg_2 = arg_list[size-1]
        if utilization_arg_2 != '0':
            load = str(round((float(utilization_arg_1)/float(utilization_arg_2))*100,2))
        else:
            load = '0'
        # print utilization_arg_1+" | "+utilization_arg_2


        child = subprocess.Popen(frequency_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=defulat_adb_tool_path)
        child.wait()
        child_out = child.stdout.readlines()
        child.stdout.close()
        location = child_out[0].find('\r')
        arg_list = child_out[0][0:location].strip()
        gpu_frequency = str(int(arg_list)/1000000)
        # print gpu_frequency

        # 将数据写入文件

        with open(os.path.join(arg_log_path, arg_device_id + "_GPU.log"), "a") as f:
            write_str = '[' + str(now_time) + ']|{"G01":"' + utilization_arg_1 + '",'+'"G02":"'+utilization_arg_2+'",' +\
                        '"Load":"'+load+'%",'+'"Frequency":"'+gpu_frequency+'MHZ"'+'} \n'
            f.write(write_str)
        time.sleep(float(arg_collect_time))


def check_device(arg_device_id):
    cmd = [os.path.join(defulat_adb_tool_path, "adb"), "devices"]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=defulat_adb_tool_path)
    child.wait()
    child_out = child.stdout.readlines()
    child.stdout.close()

    flag = False
    for item in child_out:
        if item.find(arg_device_id) >= 0 and item.find("offline") < 0:
            flag = True
            break

    return flag


def main():
    global defulat_adb_tool_path
    adb_path = os.environ.get('ANDROID_HOME')
    if os.path.isdir(os.path.join(adb_path, "platform-tools")):
        defulat_adb_tool_path = os.path.join(adb_path, "platform-tools")
    else:
        print u"请设置‘ANDROID_HOME’环境变量"
        sys.exit(0)
    # 定义argparse
    parser = argparse.ArgumentParser(description='获取进程的CPU占用脚本')
    parser.add_argument('--collect-time', dest='collect_time', required=True, help='信息采集间隔，以秒为单位，整数')
    parser.add_argument('--log-path', dest='log_path', required=True, help='日志文件的放置位置')
    parser.add_argument('--device-id', dest='device_id', required=True, help='设备序列号')
    args = parser.parse_args()
    # 获取参数
    param_collect_time = args.collect_time
    param_log_path = args.log_path
    param_device_id = args.device_id
    # 检测是设备是否存在
    if check_device(param_device_id) is False:
        print U"设备序列号不存在或离线"
        sys.exit(0)
    # 开始采集信息
    collect_msg(param_collect_time, param_log_path, param_device_id)


if __name__ == "__main__":
    main()