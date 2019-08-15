# -*- coding:utf-8 -*-
import argparse
import os
import time
import csv
import traceback
import subprocess
from multiprocessing.dummy import Pool as ThreadPool

PHONE_NAME  = {
    'Coolpad8297W': 'kpyy',
    'A37': 'oppoyy',
    'hwG750-T00': 'hw3xyy',
    'HM2013023': 'hmyy',
    'lcsh92_wet_tdd': 'hmnoteyy',
    'mx3': 'mzyy',
    'bbk92_wet_jb9': 'voyy',
    'hwp7': 'hwp7yy',
}


class CsvLine(object):
    def __init__(self, args_text):
        if args_text is None:
            raise ValueError("Text can't be None")

        if not isinstance(args_text, list):
            raise TypeError("Text should be list")

        self.text = args_text

    def append_text(self, args_text):
        self.text.append(args_text)

    def push_text(self, args_text):
        self.text.insert(0, args_text)

    def get_text(self):
        return self.text


class LineWithTimeStep(CsvLine):
    def __init__(self, args_text):
        CsvLine.__init__(self, args_text=args_text)
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.push_text(now_time)


class CsvWriter(object):
    def __init__(self, args_file_path):
        self.file_path = args_file_path
        self.file_handler = None
        self.csv_handler = None

    def open_file(self):

        self.file_handler = open(self.file_path, 'ab')
        self.csv_handler = csv.writer(self.file_handler)

    def close_file(self):
        if self.file_handler:
            self.file_handler.close()

    def write_line(self, args_line):

        if not isinstance(args_line, CsvLine):
            raise TypeError(
                "Need a Line object instead of {}, when write to {}".format(type(args_line), self.file_path))
        self.csv_handler.writerow(args_line.get_text())


class PerfGetter(object):
    def __init__(self, args_file_path):

        self.csv_writer = CsvWriter(args_file_path=args_file_path)

    def run(self):
        try:
            self.csv_writer.open_file()
            self.execute_command()
        except Exception:
            traceback.print_exc()
        finally:
            self.csv_writer.close_file()

    def execute_command(self):
        pass


class CpuGetter(PerfGetter):
    DEFAULT_DELAY = "3"

    def __init__(self, args_file_path, args_process_name):
        PerfGetter.__init__(self, args_file_path=args_file_path)
        self.process_name = args_process_name

    def execute_command(self):
        cpu_line = 0
        try:
            top_info = Utils.get_top_info(CpuGetter.DEFAULT_DELAY, self.process_name)
            top_line = CpuGetter.TopLine(top_info)
            cpu_line = LineWithTimeStep([top_line.get_cpu_info()])
        except Exception:
            traceback.print_exc()
        finally:
            self.csv_writer.write_line(cpu_line)

    class TopLine(object):
        def __init__(self, line):
            items = line.split()
            self.__pid = items[0]
            self.__cpu_info = items[2].replace("%", "")
            self.__process_info = items[len(items) - 1]

        def get_cpu_info(self):
            return self.__cpu_info

        def get_pid(self):
            return self.__pid

        def get_process_info(self):
            return self.__process_info


class GpuGetter(PerfGetter):
    def __init__(self, args_file_path):
        PerfGetter.__init__(self, args_file_path=args_file_path)

    def execute_command(self):
        g01 = 0
        g02 = 0
        load = 0
        frq = 0

        try:
            busy_info = subprocess.check_output(Utils.get_command_with_device_id(['cat','/sys/class/kgsl/kgsl-3d0/gpubusy']))
            clk_info = subprocess.check_output(Utils.get_command_with_device_id(['cat', '/sys/class/kgsl/kgsl-3d0/gpuclk']))
            
            if "No such file or directory" in busy_info or "No such file or directory" in clk_info:
                raise ValueError("No gpubusy file or gpuclk")

            busy_info_list = busy_info.split()

            g01 = busy_info_list[0]
            g02 = busy_info_list[1]

            if g02 == '0':
                load = 0
            else:
                load = round((float(g01) / float(g02)) * 100, 2)

            frq = int(clk_info) / 1000000

        except Exception:
            traceback.print_exc()
        finally:
            self.csv_writer.write_line(LineWithTimeStep([g01, g02, load, frq]))


class BatteryGetter(PerfGetter):
#    FILTER_TEMP = "POWER_SUPPLY_TEMP"
#    FILTER_CAPACITY = "POWER_SUPPLY_CAPACITY"
    FILTER_TEMP = "temperature"
    FILTER_CAPACITY = "level"

    def __init__(self, args_file_path):
        PerfGetter.__init__(self, args_file_path=args_file_path)

    def execute_command(self):
        temp = 0
        capacity = 0
        try:
#            battery_info = subprocess.check_output(Utils.get_command_with_device_id(['cat','/sys/class/power_supply/battery/uevent']))
            battery_info = subprocess.check_output(Utils.get_command_with_device_id(['dumpsys','battery']))

            lines = battery_info.splitlines()
            
            for line in lines:
                battery_file_line = BatteryGetter.BatteryFileLine(line)
                if battery_file_line.get_key() == BatteryGetter.FILTER_TEMP and temp == 0:
                    temp = battery_file_line.get_value()
                elif battery_file_line.get_key() == BatteryGetter.FILTER_CAPACITY and capacity == 0 :
                    capacity = battery_file_line.get_value()
        except Exception:
            traceback.print_exc()
        finally:
            self.csv_writer.write_line(LineWithTimeStep([temp, capacity]))

    class BatteryFileLine(object):

        DELIMITER = ":"

        def __init__(self, args_battery_info_line):
            items = args_battery_info_line.strip().split(BatteryGetter.BatteryFileLine.DELIMITER)
            self.__key = items[0].strip()
            self.__value = items[1].strip()

        def get_key(self):
            return self.__key

        def get_value(self):
            return self.__value


class FlowGetter(PerfGetter):
    DEFAULT_DELAY = 0

    def __init__(self, args_file_path, args_process_name):
        PerfGetter.__init__(self, args_file_path=args_file_path)
        self.process_name = args_process_name

    def execute_command(self):
        recv = 0
        trans = 0
        try:
            top_info = Utils.get_top_info(CpuGetter.DEFAULT_DELAY, self.process_name)
            pid = CpuGetter.TopLine(top_info).get_pid()
            flow_info = subprocess.check_output(
                Utils.get_command_with_device_id(["cat", "/proc/" + pid + "/net/dev", "|", "grep", "wlan0"]))

            flow_file_line = FlowGetter.FlowFileLine(flow_info)
            recv = flow_file_line.get_recv()
            trans = flow_file_line.get_trans()
        except Exception:
            traceback.print_exc()
        finally:
            self.csv_writer.write_line(LineWithTimeStep([str(time.time()), recv, trans]))

    class FlowFileLine(object):
        def __init__(self, line):
            items = line.split()
            self.__recv = items[1]
            self.__trans = items[9]

        def get_recv(self):
            return self.__recv

        def get_trans(self):
            return self.__trans


class Utils(object):
    PATH = "default"
    DEVICE_ID = "default"
    DEVICE_NAME = "default"
    APP_NAME = "default"
    TIMES = "default"
    FILE_TYPE = "csv"

    @staticmethod
    def init(args_path, args_device_id, args_app_name, args_times, args_device_name,arg_client):
        Utils.PATH = args_path
        Utils.DEVICE_ID = args_device_id
        Utils.APP_NAME = args_app_name
        Utils.TIMES = args_times
        Utils.DEVICE_NAME = args_device_name
        Utils.CLIENT = arg_client

    @staticmethod
    def get_top_info(args_delay, process_name):
        output = subprocess.check_output(
            Utils.get_command_with_device_id(['top', '-d', args_delay, '-n', '1', '|', 'grep', process_name]))
        lines = output.splitlines()
        for line in lines:
            if line.endswith(process_name):
                return line

        raise ValueError("Can't find process info from top by greping {}".format(process_name))

    @staticmethod
    def get_command_with_device_id(args_command_list):
        result_command = ['adb', '-s', Utils.DEVICE_ID, 'shell']
        result_command.extend(args_command_list)
        return result_command

    @staticmethod
    def get_absolute_file_name(args_perf_type):
        return os.path.join(Utils.PATH, "{}_android_{}_{}.{}".format(PHONE_NAME.get(Utils.DEVICE_NAME), #Utils.APP_NAME,
                                                                Utils.CLIENT + args_perf_type, Utils.TIMES, Utils.FILE_TYPE))
        # return os.path.join(Utils.PATH, "{}_{}_{}_{}.{}".format(Utils.DEVICE_NAME, Utils.APP_NAME,
        #                                                         args_perf_type, Utils.TIMES, Utils.FILE_TYPE))



def main():
    # 定义argparse
    parser = argparse.ArgumentParser(description='获取android性能脚本', epilog="python path/perf_getter.py "
                                                                         "/User/wenli/Desktop 01 usb:337641472X s7 "
                                                                         "com.duowan.mobile yy -i 5 -d 1800")
    parser.add_argument('path', help='文件的放置目录')
    parser.add_argument('times', help='采集次数，用于建立文件夹与文件命名')
    parser.add_argument('device_id', help='设备序列号或者usb序号')
    parser.add_argument('device_name', help='设备名字')
    parser.add_argument('package_name', help='应用包名')
    parser.add_argument('app_name', help='应用别名')
    parser.add_argument('client', help='客户端：actor，viewer')
    parser.add_argument('-i', '--interval', default=5, help='信息采集间隔，以秒为单位，默认5秒', type=int)
    parser.add_argument('-d', '--duration', default=1800, help='信息采集总时常，以秒为单位，默认1800秒', type=int)

    args = parser.parse_args()

    # 获取参数
    path = args.path
    times = args.times
    device_id = args.device_id
    device_name = args.device_name
    package_name = args.package_name
    app_name = args.app_name
    interval = args.interval
    duration = args.duration
    client = args.client

    # path = "/Users/wenli/yy/201708/test_csv_writer"
    # times = "01"
    # device_id = "usb:337641472X"
    # device_name = "s7"
    # package_name = "com.duowan.mobile"
    # app_name = "yy"
    # interval = 5
    # duration = 30

    dir_name = os.path.join(path, device_name, times)

    # 初始化utils类
    Utils.init(args_path=dir_name, args_device_id=device_id, args_app_name=app_name, args_times=times,
               args_device_name=device_name, arg_client=client)

    # 检查路径给出的文件夹是否存在，不存在则创建
    if not os.path.exists(dir_name):
        print ("{} 文件夹不存在，创建文件夹".format(dir_name))
        os.makedirs(dir_name)

    # 初始化各类采集实例
    app_cpu_getter = CpuGetter(Utils.get_absolute_file_name("cpu"), package_name)
    mediaserver_cpu_getter = CpuGetter(
        Utils.get_absolute_file_name("mediaservercpu"), "mediaserver")
    gpu_getter = GpuGetter(Utils.get_absolute_file_name("gpu"))
    battery_getter = BatteryGetter(Utils.get_absolute_file_name("battery"))
    flow_getter = FlowGetter(Utils.get_absolute_file_name("network"), package_name)

    getter_list = [app_cpu_getter, mediaserver_cpu_getter, gpu_getter, battery_getter, flow_getter]

    # 需要跑几个线程来分别做这几个事情
    pool_size = 5
    pool = ThreadPool(pool_size)

    while duration > 0:
        func_map = pool.map_async(lambda x: x.run(), getter_list)
        time.sleep(interval)
        duration -= interval
        func_map.wait()

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
