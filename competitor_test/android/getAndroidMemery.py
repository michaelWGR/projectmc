# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time
import argparse

defulat_adb_tool_path = "D:\\developSdk\\Android\\sdk\\platform-tools"


def collect_msg(arg_time, arg_log_path, arg_app_name, arg_device_id):
    # 根据应用的包名称 获取CPU以及内存占用+
    app_id_str = ""
    memory_str = ""
    while 1:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        cpu_memery_cmd = [os.path.join(defulat_adb_tool_path, "adb"), "-s", arg_device_id, "shell", "top", "-m", "10", "-n", "1"]
        child = subprocess.Popen(cpu_memery_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=defulat_adb_tool_path)
        child.wait()
        child_out = child.stdout.readlines()
        child.stdout.close()
        for item in child_out:

            if item.find(arg_app_name) > 0:
                if item.find("K") > 0:  # 获取内存占用
                    tmp_memory = item[item.find("K") + 1:]
                    last_location = tmp_memory.find("K")
                    memory_str = str(int(tmp_memory[0:last_location]))

                break
        with open(os.path.join(arg_log_path, arg_device_id + "_" + arg_app_name + "_memory.log"), "a") as f:
            write_str = '[' + str(
                now_time) + ']|{"memory":"' + memory_str + 'K"} \n'
            f.write(write_str)

        time.sleep(float(arg_time))


def check_device(arg_device_id):
    cmd = [os.path.join(defulat_adb_tool_path, "adb"),"devices"]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=defulat_adb_tool_path)
    child.wait()
    child_out = child.stdout.readlines()
    child.stdout.close()

    flag = False;
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
    parser.add_argument('--package-name', dest='pachage_name', required=True, help='应用的包名')
    parser.add_argument('--device-id', dest='device_id', required=True, help='设备序列号')
    args = parser.parse_args()
    # 获取参数
    param_collect_time = args.collect_time
    param_log_path = args.log_path
    param_package_name = args.pachage_name
    param_device_id = args.device_id
    # 检测是设备是否存在
    if check_device(param_device_id) is False:
        print U"设备序列号不存在或离线"
        sys.exit(0)
    collect_msg(param_collect_time, param_log_path, param_package_name, param_device_id)

if __name__ == '__main__':
    main()