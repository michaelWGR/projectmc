#!/usr/bin/env python
# -*- coding:utf-8 -*-


import subprocess
import argparse
import os
import time
import ftplib
import requests
import sys
from ftplib import FTP
from colorama import init as color_init, Fore

color_init()

"""
adb shell dumpsys window windows | grep -E 'mCurrentFocus'

yy: mCurrentFocus=Window{dea78f7 u0 com.duowan.mobile/com.yy.mobile.ui.home.MainActivity}
hy: mCurrentFocus=Window{6cbb508 u0 com.duowan.kiwi/com.duowan.kiwi.homepage.Homepage}
mo: mCurrentFocus=Window{f8e53db u0 com.immomo.momo/com.immomo.momo.maintab.MaintabActivity}
yk; mCurrentFocus=Window{ad5b889 u0 com.meelive.ingkee/com.meelive.ingkee.business.main.ui.MainActivity}
xm: mCurrentFocus=Window{823925b u0 com.wali.live/com.wali.live.main.LiveMainActivity}
bg: mCurrentFocus=Window{e75cc48 u0 sg.bigo.live/com.yy.iheima.FragmentTabs}
lm: mCurrentFocus=Window{5f80c36 u0 com.cmcm.live/com.cmcm.cmlive.activity.VideoListActivity}
dy: mCurrentFocus=Window{2ee0c143 u0 air.tv.douyu.android/tv.douyu.view.activity.MainActivity}
pd: mCurrentFocus=Window{3cdd7ff6 u0 com.panda.videoliveplatform/com.panda.videoliveplatform.activity.MainFragmentActivity}
cs: mCurrentFocus=Window{19bf2724 u0 com.android.settings/com.android.settings.Settings$DevelopmentSettingsActivity}
"""

# print '\033[1;31;40m' + str + '\033[0m'

DIR_NOT_FOUND_ERROR = '550 The system cannot find the file specified.'

PROCESS_NAME_DICT = {
    'com.duowan.mobile': 'yy',
    'com.duowan.kiwi': 'hy',
    'com.immomo.momo': 'mo',
    'com.meelive.ingkee': 'yk',
    'com.wali.live': 'xm',
    'sg.bigo.live': 'bg',
    'com.cmcm.live': 'lm',
    'air.tv.douyu.android': 'dy',
    'com.panda.videoliveplatform': 'pd',
    'com.android.settings': 'cs'
}

SWIPE_SPEED = {
    'yy': 100,
    'hy': 100,
    'mo': 100,
    'yk': 100,
    'xm': 100,
    'bg': 100,
    'lm': 100,
    'dy': 100,
    'pd': 100,
}

LIST_URL = 'http://results.yypm.com/management/suite/list.json?page_num=1'


class EnvironmentInit(object):
    def __inti__(self):
        self.app = None
        self.package_name = None
        self.width = None
        self.height = None

    def getApp(self):
        cmd = 'adb shell dumpsys window windows'.split()
        child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        # child.wait()
        # stdout,_ = child.communicate()

        while True:
            line = child.stdout.readline()
            if 'mCurrentFocus' in line:
                for key in PROCESS_NAME_DICT:
                    if key in line:
                        self.app = PROCESS_NAME_DICT.get(key, None)
                        self.package_name = key
            if line == '' and child.poll():
                break


class FtpHandler(object):
    def __init__(self, arg_host='192.168.31.209', arg_user='root', arg_password='', arg_login_anonymous=False):
        self.user = arg_user
        self.password = arg_user
        self.ftp_client = FTP()
        self.ftp_client.connect(arg_host, '22')
        self.folders = []
        try:
            if arg_login_anonymous:
                self.ftp_client.login()
            else:
                self.ftp_client.login(self.user, self.password)
        except Exception, e:
            raise 'create connect faile, error:' + e

    def _mkd_or_cwd(self, arg_folder):
        """
            give a folder,mkdir if cd faile with director not exits
        """
        try:
            self.ftp_client.cwd(arg_folder)
        except ftplib.all_errors, e:
            if '550' in str(e):
                self.ftp_client.mkd(arg_folder)
                self.ftp_client.cwd(arg_folder)

    def cwd_path(self, arg_abs_path):
        """
        cd into target path
        """
        sp = arg_abs_path
        self.ftp_client.cwd('/')
        while os.path.split(sp)[1] != '':
            self.folders.insert(0, os.path.split(sp)[1])
            sp = os.path.split(sp)[0]

        for folder in self.folders:
            self._mkd_or_cwd(folder)
        self.folders = []

    def send_file(self, arg_filename, arg_file_path):
        """
        upload target file to target path
        """
        self.ftp_client.storbinary("STOR " + arg_filename, open(arg_file_path, 'rb'))


class OperateUnit(object):
    def __init__(self, arg_width, arg_height):
        self.width = arg_width
        self.height = arg_height

    def pull_to_local(self, arg_remote_path, arg_local_path):
        cmd = ['adb', 'pull', arg_remote_path, arg_local_path]
        p = subprocess.Popen(cmd)
        p.wait()

    def delete_remote(self, arg_remote_path):
        cmd = ['adb', 'shell', 'rm', arg_remote_path]
        p = subprocess.Popen(cmd)
        p.wait()

    def operate(self, arg_time):
        pass

    def run(self, arg_time):
        pass


class ListOperateUnit(OperateUnit):
    def __init__(self, arg_app, arg_output_dir, arg_width, arg_height):
        super(ListOperateUnit, self).__init__(arg_width, arg_height)
        self.app = arg_app
        self.output_dir = arg_output_dir
        self.file_name = None

        self.start_x_percentage = 0.5
        self.start_y_percentage = 0.15
        self.end_x_percentage = 0.5
        self.end_y_percentage = 0.925

    def swipe_to_top(self):
        """
            循环4次向上拉，保证到达顶部
        """
        start_x = 0.5 * float(self.width)
        start_y = 0.15 * float(self.height)
        end_x = 0.5 * float(self.width)
        end_y = 0.925 * float(self.height)
        for i in (0, 4):
            op_cmd = "adb shell input swipe {} {} {} {} 150".format(int(start_x), int(start_y), int(end_x),
                                                                    int(end_y)).split()
            o_p = subprocess.Popen(op_cmd)
            o_p.wait()

    def operate(self, arg_time):

        self.file_name = '{}_android_list_{}.mp4'.format(self.app, str(arg_time).zfill(2))
        self.remote_path = "/sdcard/" + self.file_name
        self.local_path = os.path.join(self.output_dir, self.file_name)
        start_x = self.start_x_percentage * float(self.width)
        start_y = self.start_y_percentage * float(self.height)
        end_x = self.end_x_percentage * float(self.width)
        end_y = self.end_y_percentage * float(self.height)
        record_cmd = 'adb shell screenrecord --bit-rate 16000000 --size {}x{} {}'.format(self.width, self.height,
                                                                                         self.remote_path).split()
        r_p = subprocess.Popen(record_cmd)
        time.sleep(1)
        op_cmd = "adb shell input swipe {} {} {} {}".format(int(start_x), int(start_y), int(end_x), int(end_y)).split()
        o_p = subprocess.Popen(op_cmd)
        o_p.wait()
        # 强制等待5秒后kill
        time.sleep(5)
        r_p.terminate()
        while r_p.poll() is None:
            time.sleep(0.5)
        time.sleep(1)

    def run(self, arg_time):
        self.operate(arg_time)
        self.pull_to_local(self.remote_path, self.local_path)
        self.delete_remote(self.remote_path)
        return {'path': self.local_path, 'name': self.file_name}


class PicOperateUnit(OperateUnit):
    def __init__(self, arg_app, arg_output_dir, arg_width, arg_height):
        super(PicOperateUnit, self).__init__(arg_width, arg_height)
        self.app = arg_app
        self.output_dir = arg_output_dir
        self.file_name = None

    def operate(self, arg_time):
        self.file_name = '{}_android_pic_{}.mp4'.format(self.app, str(arg_time).zfill(2))

        self.remote_path = "/sdcard/" + self.file_name
        self.local_path = os.path.join(self.output_dir, self.file_name)
        start_x = 0.5 * float(self.width)
        start_y = 0.8 * float(self.height)
        end_x = 0.5 * float(self.width)
        end_y = 0.125 * float(self.height)
        record_cmd = "adb shell screenrecord --bit-rate 16000000 --size {}x{} {}".format(self.width, self.height,
                                                                                         self.remote_path).split()
        r_p = subprocess.Popen(record_cmd)
        time.sleep(1)

        op_cmd = "adb shell input swipe {} {} {} {} 150".format(int(start_x), int(start_y), int(end_x),
                                                                int(end_y)).split()
        o_p = subprocess.Popen(op_cmd)
        o_p.wait()
        time.sleep(2)
        r_p.terminate()
        while r_p.poll() is None:
            time.sleep(0.5)
        time.sleep(1)

    def run(self, arg_time):
        self.operate(arg_time)
        self.pull_to_local(self.remote_path, self.local_path)
        self.delete_remote(self.remote_path)
        return {'path': self.local_path, 'name': self.file_name}


class StartOperateUnit(OperateUnit):
    def __init__(self, arg_app, arg_output_dir, arg_width, arg_height):
        super(StartOperateUnit, self).__init__(arg_width, arg_height)
        self.app = arg_app
        self.output_dir = arg_output_dir
        self.file_name = None

    def kill_process(self, arg_package_name):
        kill_cmd = 'adb shell am force-stop {}'.fotmat(arg_package_name)
        child = subprocess.Popen(cmd)
        child.terminate()

    def goto_home(self):
        kill_cmd = 'adb shell input keyevent 3'
        child = subprocess.Popen(cmd)
        child.terminate()

    def swipe_left(self):
        start_x = 0.9 * float(self.width)
        start_y = 0.5 * float(self.height)
        end_x = 0.1 * float(self.width)
        end_y = 0.5 * float(self.height)
        swipe_cmd = 'adb shell input swipe {} {} {} {} 50'.fotmat(int(start_x, start_y, end_x, end_y))
        child = subprocess.Popen(cmd)
        child.terminate()

    def get_app_location(self, arg_app_name):
        pass

    def operate(self, arg_time, arg_package_name):
        pass

    def run(self):
        pass


def get_cur_running_process():
    cmd = 'adb shell dumpsys window windows'.split()
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    # child.wait()
    stdout, _ = child.communicate()

    lines = stdout.splitlines()

    for line in lines:
        if 'mCurrentFocus' in line:
            for key in PROCESS_NAME_DICT:
                if key in line:
                    return PROCESS_NAME_DICT.get(key, None)

    # while True:
    #     line = child.stdout.readline()
    #     if 'mCurrentFocus' in line:
    #         for key in PROCESS_NAME_DICT:
    #             if key in line:
    #                 return PROCESS_NAME_DICT.get(key, None)
    #     if line == '' or child.poll():
    #         break
    return None


def get_resolution():
    cmd = 'adb shell wm size'.split()
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = child.communicate()
    words = stdout.split(' ')
    res = words[-1].replace('\r', '').replace('\n', '')
    width, height = res.split('x')
    return width, height


def pull_file(arg_remote_path, arg_local_path):
    cmd = ['adb', 'pull', arg_remote_path, arg_local_path]
    p = subprocess.Popen(cmd, )
    p.wait()


def delete_file(arg_remote_path):
    cmd = ['adb', 'shell', 'rm', arg_remote_path]
    p = subprocess.Popen(cmd)
    p.wait()


def list_operation(arg_width, arg_height, arg_file_name):
    start_x = 0.5 * float(arg_width)
    start_y = 0.125 * float(arg_height)
    end_x = 0.5 * float(arg_width)
    end_y = 0.9 * float(arg_height)
    record_cmd = 'adb shell screenrecord --bit-rate 16000000 --size {}x{} {}'.format(arg_width, arg_height,
                                                                                     arg_file_name).split()
    r_p = subprocess.Popen(record_cmd)
    time.sleep(1)
    op_cmd = "adb shell input swipe {} {} {} {}".format(int(start_x), int(start_y), int(end_x), int(end_y)).split()
    o_p = subprocess.Popen(op_cmd)
    o_p.wait()
    # 强制等待5秒后kill
    time.sleep(5)
    r_p.kill()
    # r_p.terminate()
    time.sleep(2)


def pic_operation(arg_width, arg_height, arg_file_name):
    start_x = 0.5 * float(arg_width)
    start_y = 0.8 * float(arg_height)
    end_x = 0.5 * float(arg_width)
    end_y = 0.125 * float(arg_height)
    record_cmd = "adb shell screenrecord --bit-rate 16000000 --size {}x{} {}".format(arg_width, arg_height,
                                                                                     arg_file_name).split()
    r_p = subprocess.Popen(record_cmd)
    time.sleep(1)

    op_cmd = "adb shell input swipe {} {} {} {} 150".format(int(start_x), int(start_y), int(end_x), int(end_y)).split()
    o_p = subprocess.Popen(op_cmd)
    o_p.wait()
    # 强制等待5秒后kill
    time.sleep(2)
    r_p.kill()
    # r_p.terminate()
    time.sleep(2)


def check_environment():
    dict_ = {
        '1': 'mobile',
        '2': 'game',
        '3': 'shortvideo',
        '4': 'lowmobile',
        '5': 'assist',
    }
    selection = raw_input('选择suite类型: 1: 移动直播, 2: 游戏直播, 3: 短时频, 4: 低端机, 5: 手游直播:')
    suite_type = dict_.get(selection)

    count = 0
    right_suite = None
    re = requests.get(LIST_URL)

    if re.status_code == 200:
        re = re.json()
        if re.get('code') == 0:
            suites = re.get('result').get('suites')
            for suite in suites:
                if suite.get('status') in (0, 1) and suite.get('suite_type') == suite_type:
                    right_suite = suite
                    count += 1
    if count != 1:
        print(Fore.RED + '该suite type 类型的suite数量不为1，为：' + str(count))
        return None
    else:
        return '{}_{}'.format(right_suite.get('id'), right_suite.get('suite_type'))


def main():
    argparser = argparse.ArgumentParser('list and pic recorder')
    argparser.add_argument('--start_time', type=int, default=1, help='start video time default: 1')
    argparser.add_argument('--record_times', type=int, default=6, help='collect count, default: 6')
    argparser.add_argument('--ob', default=None, help='output base dir')
    argparser.add_argument('collect_case', help='collect case: list,pic,all')

    args = argparser.parse_args()

    start_num = args.start_time
    record_times = start_num + args.record_times
    output_dir = args.ob if args.ob is not None else os.getcwd()
    collect_case = args.collect_case

    if collect_case not in ('list', 'pic', 'all'):
        print(Fore.RED + 'collect case error')
        return

    id_type = check_environment()

    if id_type is None:
        return
    app = get_cur_running_process()
    if app is None:
        print(Fore.RED + '应用环境不正确，请确认')
        return

    if 'assist' in id_type and app not in ('cs'):
        app = app + 'assist'

    width, height = get_resolution()

    list_file_name = '{}_android_list_{}.mp4'
    pic_file_name = '{}_android_pic_{}.mp4'
    wait_upload = []

    # collect list
    if collect_case in ('list', 'all'):
        operate_unit = ListOperateUnit(app, output_dir, width, height)
        for i in range(start_num, record_times):
            # file_name = list_file_name.format(app, str(i).zfill(2))
            # remote_path = "/sdcard/" + file_name
            # local_path = os.path.join(output_dir, id_type, file_name)

            # list_operation(width, height, remote_path)
            # pull_file(remote_path, local_path)
            # delete_file(remote_path)

            # wait_upload.append({'path': local_path, 'name': file_name})
            wait_upload.append(operate_unit.run(i))

    # collect pic
    if collect_case in ('pic', 'all'):
        operate_unit = PicOperateUnit(app, output_dir, width, height)
        for i in range(start_num, record_times):
            # file_name = pic_file_name.format(app, str(i).zfill(2))
            # remote_path = "/sdcard/" + file_name
            # local_path = os.path.join(output_dir, id_type, file_name)

            # pic_operation(width, height, remote_path)
            # pull_file(remote_path, local_path)
            # delete_file(remote_path)

            # wait_upload.append({'path': local_path, 'name': file_name})

            wait_upload.append(operate_unit.run(i))

    # upload

    # ftp_path = '/' + id_type
    # try:
    #     ftp_client = FtpHandler('192.168.31.209', arg_login_anonymous=True)
    #     ftp_client.cwd_path(ftp_path)
    # except Exception, e:
    #     print(Fore.RED + 'connect to ftp server: 192.168.31.209 error')
    #     print(e)
    # for item in wait_upload:
    #     try:
    #         ftp_client.send_file(item.get('name'), item.get('path'))
    #     except Exception, e:
    #         print(Fore.RED + 'file: {} upload error'.format(item.get('name')))
    #         print(e)


if __name__ == '__main__':
    main()
