# -*- coding:utf-8 -*-
from subprocess import Popen
from subprocess import PIPE
from ftplib import FTP
from record_tool_util import *
from record_tool_setting import *
from record_tool_environment import *
import json
import os
import datetime
import time
import shutil
import logging

logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(data_dir, 'upload.log'),
                        filemode='a')


class App(object):


    @classmethod
    def get_apps(cls, task_id, app_filter):
        apps= []

        if app_filter is not None:
            sql_str = 'select app_id from suite_app where suite_id=' + str(task_id)
            app_ids = SqlTool().execute_query(sql_str)
            for app_id in app_ids:
                app = SqlTool().execute_query("select * from apps where (id=" + str(app_id[0]) + " and display_name like '%" + app_filter + "%') or (id="+str(app_id[0])+" and display_name not like '%-%')")
                if len(app) > 0:
                    apps.append(app)

        return apps


class Task(object):


    @classmethod
    def get_tasks(cls):
        sql_str = 'select * from suites where status=1 order by ctime desc'
        tasks = SqlTool().execute_query(sql_str)
        return tasks


    @classmethod
    def get_task_type(cls,task_id):
        sql_str = 'select suite_type from suites where id=%s' %task_id
        suite_type = SqlTool().execute_query(sql_str)[0][0]
        return suite_type


class Case(object):


    @classmethod
    def get_cases(cls, task_id):
        cases= []

        sql_str = 'select case_id from suite_case where suite_id=' + str(task_id)
        case_ids = SqlTool().execute_query(sql_str)

        for case_id in case_ids:
            case = SqlTool().execute_query('select * from cases where id=%s'%(str(case_id[0])))
            if json.loads(case[0][6])['android'] == 'frametime':
                if case[0][9] is None:
                    cases.append(case[0])

        return cases


class ResultOrder(object):

    order_map = dict()

    @classmethod
    def hold_order(cls, task_id, case_id, platform, app_id):
        for i in range(100):
            order = cls.get_order(task_id, case_id, platform, app_id) + 1
            result = cls.update_order(task_id, case_id, platform, app_id, order)

            if result == 1:
                key = '%s_%s_%s_%s' %(task_id, case_id, platform, app_id)
                cls.order_map[key] = order
                return order

    @classmethod
    def get_order(cls, task_id, case_id, platform, app_id):
        sql_str = "select `order` from result_orders where suite_id='%s' and cass_id='%s' and platform='%s' and app_id='%s'" % (
        task_id, case_id, platform, app_id)
        results = SqlTool().execute_query(sql_str)
        order = 0

        if len(results) == 0:
            ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            SqlTool().execute_update("insert into result_orders values('%s','%s','%s','%s','%s','%s','%s')" % (
            task_id, case_id, platform, app_id, 0, ctime, ctime))
        else:
            order = results[0][0]

        return order


    @classmethod
    def update_order(cls, task_id, case_id, platform, app_id, new_order):
        mtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_str = "update result_orders set`order`=%s,mtime='%s' where suite_id=%s and cass_id=%s and platform='%s' and app_id=%s and `order`=%s"%(new_order, mtime ,task_id, case_id, platform, app_id, int(new_order) - 1)
        result = SqlTool().execute_update(sql_str)
        return result


class Record(object):
    """
    status状态
        0 : 开始录制
        1 : 拖出成功
        2 : 拖出失败
        3 : 设备未连接
        4 : 设备未授权
        5 : 设备未知错误
        6 : 连接了多台设备
    """
    sub_process = None
    status = 0

    @classmethod
    def start_record(cls,model):
        Record.status = 0
        Popen('adb shell rm -r /sdcard/recorders'.split(), stdout=PIPE, stderr=PIPE).wait()
        Popen('adb shell mkdir /sdcard/recorders'.split(), stdout=PIPE, stderr=PIPE).wait()
        args = None
        system_version = Phone.get_system_version()
        for argument in record_args:
            if argument.get('model') == model and argument.get('system') is None:
                args = argument.get('args')
            elif argument.get('model') is None and argument.get('system')==system_version:
                args = argument.get('args')
            elif argument.get('model')==model and argument.get('system')==system_version:
                args = argument.get('args')

            if args is not None:
                break

        if args is None:
            args = default_record_args

        command = 'adb shell screenrecord %s /sdcard/recorders/temp.mp4' %args
        print command
        cls.sub_process = Popen(command.split(),stdout=PIPE,stderr=PIPE)

        info = str(cls.sub_process.communicate())
        if 'failed' in info or 'erro' in info or 'Erro' or 'not found'in info:
            Record.status = 5

        print '视频录制的ADB信息:'
        print info
        print


    @classmethod
    def finish_record(cls, app_name, platform, task_id, case_name, order):
        time.sleep(1)

        if cls.sub_process is not None and cls.sub_process.poll() is None:
            cls.sub_process.terminate()
            cls.pull_video(app_name, platform, task_id, case_name, order)
        else:
            if(Record.status == 0):
                Record.status = 3


    @classmethod
    def pull_video(cls, app_name, platform, task_id, case_name, order):
        time.sleep(2)

        video_name = '%s_%s_%s_%s.mp4'%(app_name, platform, case_name, "{:02d}".format(order))

        path = os.path.join(data_dir, 'videos', '%s'%(task_id))
        print '视频存储路径:%s\n' %path

        temp_dir = os.path.join(path, 'temp')

        temp_recorders_dir = os.path.join(temp_dir, 'recorders')
        if not os.path.exists(temp_recorders_dir):
            os.makedirs(temp_recorders_dir)
        if 'Windows' in operate_system:
            command = 'adb pull /sdcard/recorders/ %s'%(temp_recorders_dir)
        elif "Darwin" in operate_system:
            command = 'adb pull /sdcard/recorders/ %s'%(temp_dir)

        sub_process = Popen(command.split(),stdout=PIPE,stderr=PIPE)
        sub_process.wait()

        info = str(sub_process.communicate())
        print '拖视频的ADB信息:\n%s' %info
        print '视频拖动结果:'

        if 'device' not in info:
            files = os.listdir(temp_recorders_dir)
            if len(files)==1:
                shutil.copyfile(os.path.join(temp_recorders_dir, files[0]), os.path.join(path, video_name))
                shutil.rmtree(temp_dir)
                Popen('adb shell rm -r /sdcard/recorders'.split(), stdout=PIPE, stderr=PIPE).wait()
                print 'pull success'
                Record.status = 1

            else :
                Popen('adb shell rm -r /sdcard/recorders'.split(), stdout=PIPE, stderr=PIPE).wait()
                shutil.rmtree(temp_dir)

                print 'pull failed'
                Record.status = 2
        else:
            print info
            if 'device' in info:
                Record.status = 3
            else:
                Record.status = 5


class Phone(object):


    @classmethod
    def get_phone_model(cls):
        sub_process = Popen('adb shell getprop | grep ro.product.model]'.split(), stdout=PIPE, stderr=PIPE)
        err = sub_process.stderr.read().strip()

        if len(err) == 0:
            model = sub_process.stdout.read().strip()
            try:
                model = model.split(':')[1]
                model = model[2:model.index(']')]
            except BaseException, e:
                pass

            temp = model_name_map.get(model)
            if temp is not None:
                return temp

            return model
        else:
            if 'unauthorized' in err:
                err = '设备未授权!'
            elif 'more than one' in err:
                err = '只能连接一台设备!'
            elif 'device' in err:
                err = '设备未连接!'
            else:
                err = '设备未知错误!'
            return err


    @classmethod
    def get_system_version(cls):
        sub_process = Popen('adb shell getprop | grep ro.build.version.release]'.split(), stdout=PIPE, stderr=PIPE)

        err = sub_process.stderr.read().strip()
        if len(err) == 0:
            system_version = sub_process.stdout.read().strip()
            system_version = system_version.split(':')[1]
            system_version = system_version[2:system_version.index(']')]
            return system_version
        else:
            if 'unauthorized' in err:
                err = '设备未授权!'
            elif 'device' in err:
                err = '设备未连接!'
            else:
                err = '设备未知错误!'
            return err


class Upload(object):

    json_path = os.path.join(config_dir, 'ftp.json')
    json_file = None
    try:
        json_file = open(json_path, 'r')
        data = json_file.read()
        configuration = json.loads(data)
        ip = str(configuration['ip'])
        port = str(configuration['port'])
        user = str(configuration['user'])
        password = str(configuration['password'])
    except BaseException, e:
        print'无法正确获取ftp连接参数,请在%s文件中重新配置!' % json_path
    finally:
        if json_file is not None:
            json_file.close()

    @classmethod
    def upload(cls, file):

        if os.path.exists(file):
            try:
                file_dir = os.path.dirname(file)
                file_name = os.path.basename(file)
                task_id = file_dir[file_dir.index('videos') + 7 : ]
                task_type = Task.get_task_type(task_id)

                ftp = FTP()
                # 调试级别2，显示详细信息;0为关闭调试信息
                ftp.set_debuglevel(0)

                ftp.connect(cls.ip, cls.port)
                # 登录，如果匿名登录则用空串代替即可
                ftp.login(cls.user, cls.password)

                dir = '%s_%s' %(task_id, task_type)
                try:
                    # 选择操作目录
                    ftp.cwd(dir)
                except BaseException, e:
                    ftp.mkd(dir)
                    ftp.cwd(dir)

                bufsize = 1024
                file_handler = open(file, 'rb')
                # 上传文件
                ftp.storbinary('STOR %s' % file_name, file_handler, bufsize)
                file_handler.close()
                ftp.quit()

                uploaded_dir = file_dir.replace('videos', 'uploaded_videos')
                if not os.path.exists(uploaded_dir):
                    os.makedirs(uploaded_dir)
                shutil.copyfile(file, os.path.join(uploaded_dir, file_name))
                os.remove(file)

                logging.info('文件:%s   上传结果:%s' % (file, '成功!'))
                print "上传成功！"
            except BaseException,exception:
                logging.info('文件:%s   上传结果:%s   原因:%s' % (file, '失败!', exception))
                print "上传失败！"


    @classmethod
    def get_items_to_be_uploaded(cls):
        items = []
        path = os.path.join(data_dir, 'videos')

        if os.path.exists(path):
            sub_dirs = os.listdir(path)
            for dir in sub_dirs:
                if dir[0] is not '.':

                    file_path = os.path.join(path, dir)
                    files = os.listdir(file_path)

                    for file in files:
                        if file[0] is not '.':
                            item = os.path.join(file_path, file)
                            items.append(item)

        return items


class Remake(object):


    @classmethod
    def check_remake_order(cls, task_id, app_id, platform, case_id, remake_order):

        latest_order = ResultOrder.get_order(task_id, case_id, platform, app_id)

        if remake_order<=latest_order:
            return True
        else:
            return False

class Version(object):


    @classmethod
    def get_version(cls):
        json_path = os.path.join(config_dir, 'version.json')
        json_file= None
        try:
            json_file = open(json_path, 'r')
            version_info = json_file.read()
            version = json.loads(version_info)['version']
            if 'NULL' in version:
                print'无法正确获取版本号,请在%s文件中重新配置版本号!' % json_path
            return version
        except BaseException, e:
            print'无法正确获取版本号,请在%s文件中重新配置版本号!' %json_path
        finally:
            if json_file is not None:
                json_file.close()


    @classmethod
    def set_version(cls, new_version):
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        json_path = os.path.join(config_dir, 'version.json')
        json_file = None
        try:
            json_file = open(json_path, 'w')
            version = {"version":new_version}
            json_file.write(json.dumps(version))
        except BaseException, e:
            print e
            return
        finally:
            if json_file is not None:
                json_file.close()
