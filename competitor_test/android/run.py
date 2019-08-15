# -*- coding:utf-8 -*-
import subprocess
import threading
import os
import time
import signal
import sys
import argparse

subpid = []

defulat_adb_tool_path = ''

# class Temp_cpu_Thread(threading.Thread):
#     def __init__(self, arg_collect_time, arg_log_path, arg_device_id):
#         threading.Thread.__init__(self)
#         self.collect_time = arg_collect_time
#         self.log_path = arg_log_path
#         self.device_id = arg_device_id
#     def run(self):
#         cmd = ['python', './getAndroidCpuTemperature.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,"--device-id",self.device_id]
#         child = subprocess.Popen(cmd)
#         child.wait()

# class Temp_battery_Thread(threading.Thread):
#     def __init__(self, arg_collect_time, arg_log_path, arg_device_id):
#         threading.Thread.__init__(self)
#         self.collect_time = arg_collect_time
#         self.log_path = arg_log_path
#         self.device_id = arg_device_id
#     def run(self):
#         cmd = ['python', './getAndroidBatteryTemperature.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,"--device-id",self.device_id]
#         child = subprocess.Popen(cmd)
#         child.wait()

# class Memory_Thread(threading.Thread):
#     def __init__(self, arg_collect_time, arg_log_path, arg_device_id, arg_app_package):
#         threading.Thread.__init__(self)
#         self.collect_time = arg_collect_time
#         self.log_path = arg_log_path
#         self.device_id = arg_device_id
#         self.app_package = arg_app_package
#     def run(self):
#         cmd = ['python', './getAndroidMemery.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,self.log_path,"--package-name", self.app_package,"--device-id",self.device_id]
#         child = subprocess.Popen(cmd)
#         child.wait()


class Cpu_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id, arg_app_package):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
        self.app_package = arg_app_package
    def run(self):
        cmd = ['python', './getAndroidCpu.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,
               "--package-name", self.app_package, "--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        subpid.append(child.pid)
        child.wait()

class MS_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id, arg_app_package):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
        self.app_package = arg_app_package
    def run(self):
        cmd = ['python', './getMediaServer.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,
               "--package-name", self.app_package, "--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        subpid.append(child.pid)
        child.wait()

class GPU_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
    def run(self):
        cmd = ['python', './getAndroidGPU.py', "--collect-time", self.collect_time, "--log-path", self.log_path,
               "--device-id", self.device_id]
        child = subprocess.Popen(cmd)
        subpid.append(child.pid)
        child.wait()


class Network_Thread(threading.Thread):
    def __init__(self, arg_collect_time, arg_log_path, arg_device_id, arg_app_package):
        threading.Thread.__init__(self)
        self.collect_time = arg_collect_time
        self.log_path = arg_log_path
        self.device_id = arg_device_id
        self.app_package = arg_app_package
    def run(self):
        cmd = ['python', './getAndroidNetwork.py', "--collect-time", self.collect_time,"--log-path" ,self.log_path,
               "--package-name", self.app_package,"--device-id",self.device_id]
        child = subprocess.Popen(cmd)
        subpid.append(child.pid)
        child.wait()


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

    if os.path.exists(param_log_path) == False:
        os.makedirs(param_log_path)
    # 开始采集信息
    threads = []

    temp_thread = Cpu_Thread(param_collect_time, param_log_path,param_device_id, param_package_name)
    temp_thread.start()
    threads.append(temp_thread)

    temp_thread = MS_Thread(param_collect_time, param_log_path,param_device_id, param_package_name)
    temp_thread.start()
    threads.append(temp_thread)

    temp_thread = GPU_Thread(param_collect_time, param_log_path,param_device_id)
    temp_thread.start()
    threads.append(temp_thread)

    temp_thread = Network_Thread(param_collect_time, param_log_path, param_device_id, param_package_name)
    temp_thread.start()
    threads.append(temp_thread)

    time.sleep(1830)
    for pid in subpid:
        os.kill(pid, signal.SIGTERM)
    os.kill(os.getpid(), signal.SIGINT)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()