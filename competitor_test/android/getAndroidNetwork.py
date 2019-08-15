# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time
import argparse

defulat_adb_tool_path = "D:\\developSdk\\Android\\sdk\\platform-tools"


def collect_msg(arg_collect_time, arg_log_path, arg_package_name, arg_device_id):
    # 根据应用的包名称 获取CPU以及内存占用
    app_id_str = ""
    send_network_str = ""
    rec_network_str = ""

    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    cpu_memery_cmd = [os.path.join(defulat_adb_tool_path, "adb"), "-s", arg_device_id, "shell", "top", "-n", "1", "| grep", arg_package_name]
    child = subprocess.Popen(cpu_memery_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             cwd=defulat_adb_tool_path)
    child.wait()
    child_out = child.stdout.readlines()
    child.stdout.close()
    for item in child_out:
        if item.find(arg_package_name) > 0:
            app_pid_location = item.find(" ")  # 获取app pid
            begin_find = 0
            while app_pid_location == 0:
                begin_find += 1
                app_pid_location = item[begin_find:].find(" ")
            # print app_pid_location
            app_id_str = item[begin_find:app_pid_location + begin_find]
            break
    while 1:
        # 获取流量使用情况
        now_second = time.time()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_second))
        flow_cmd = [os.path.join(defulat_adb_tool_path, "adb"), "-s", arg_device_id, "shell", "cat", "/proc/" + app_id_str + "/net/dev"]
        child = subprocess.Popen(flow_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=defulat_adb_tool_path)
        child.wait()
        child_out = child.stdout.readlines()
        child.stdout.close()
        for item in child_out:
            if item.find('wlan0') > 0:
                # print item
                begin_find = item.find(": ")
                tmp_l = 0
                last_location = item[begin_find + 2:].find(" ")
                while last_location == 0:
                    tmp_l += 1
                    last_location = item[begin_find + 2 + tmp_l :].find(" ")
                # network_str = item[begin_find + 2:last_location + begin_find + 2]  # 流量数值
                rec_network_str = str(int(item[begin_find + 2:begin_find + last_location + tmp_l + 2 ]))
                begin_find = begin_find + 2
                count_time = 0
                tmp_l = 0
                tmp_la = 0
                while count_time < 9:
                	tmp_l = 0
                	tmp_la = item[begin_find:].find(" ")
                	while tmp_la == 0:
                		tmp_l += 1
                		tmp_la = item[begin_find + tmp_l:].find(" ")
                	begin_find = begin_find + tmp_l + tmp_la
                	count_time += 1
                send_network_str = str(int(item[begin_find - tmp_la:begin_find]))
                # print item[begin_find + tmp_lo + 2:last_location + begin_find + tmp_lo + tmp_l + 2]
                # network_str = item[begin_find + 2:last_location + begin_find + 2]  # 流量数值
                break
        # 将数据写入文件

        with open(os.path.join(arg_log_path, arg_device_id + "_" + arg_package_name + "_network.log"), "a") as f:
            write_str = '[' + str(now_time) + ']|{"second":"' + str(now_second) +'","rec_data":"' + rec_network_str + \
                        'B","send_data":"' + send_network_str + 'B"} \n'
            f.write(write_str)
        time.sleep(float(arg_collect_time))


def check_device(arg_device_id):
    cmd = [os.path.join(defulat_adb_tool_path, "adb"), "devices"]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 cwd=defulat_adb_tool_path)
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
    # 开始采集信息
    collect_msg(param_collect_time, param_log_path, param_package_name, param_device_id)


if __name__ == "__main__":
    main()

