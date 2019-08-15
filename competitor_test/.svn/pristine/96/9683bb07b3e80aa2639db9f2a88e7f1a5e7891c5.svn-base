# -*- coding:utf-8 -*-
import traceback
import time
import subprocess
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool


class Device():
    def __init__(self, args_device_id, args_device_name):
        self.id = args_device_id.strip()
        self.name = args_device_name.strip()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def run_perf_command(self):
        """
        absolute_perf_getter_path : 性能获取脚本的绝对路径
        location : 结果输出的位置
        times : 第几次录制
        process_name : 测试的app包名
        app_name : app 缩写
        :return:
        """
        absolute_perf_getter_path = '/Users/luoweihoo/Desktop/201710/lowmobile/low_mobile_multi_control_scripts/perf_getter.py'
        location = '/Users/luoweihoo/Desktop/201710/lowmobile/performance/pref'
        times = '01'
        process_name = "com.duowan.mobile"
        app_name = "yy"
        client = 'viewer'
        # print ['python', absolute_perf_getter_path, '-d','1800', location, times, self.name, self.id, process_name, app_name, client]
        subprocess.check_output(
            ['python', absolute_perf_getter_path, '-d','1800', location, times, self.name, self.id, process_name, 
             app_name, client])



def get_devices():
    devices = []

    adb_devices_result = subprocess.check_output(['adb', 'devices', '-l'])

    lines = adb_devices_result.splitlines()
    first = 0

    for item in lines:
        print item
        try:
            if first > 0 and item is not None and len(item) > 0:
                devices.append(Device(item.split()[5].split(':')[1], item.split()[2]))
            first += 1
        except Exception:
            traceback.print_exc()

    return devices


def main():
    devices = get_devices()

    for device in devices:
        p = multiprocessing.Process(target=device.run_perf_command)
        p.start()



if __name__ == '__main__':
    main()
