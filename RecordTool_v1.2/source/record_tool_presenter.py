# -*- coding:utf-8 -*-
from record_tool_model import *
from record_tool_setting import *
import tkMessageBox
import threading


class AppPresenter(object):
    task_id = -1

    @classmethod
    def get_apps(cls, task_id):
        cls.task_id = task_id
        cls.apps = []

        model = Phone.get_phone_model()
        if '设备' not in model:
            app_filter = model_app_map.get(model)
            cls.apps = App.get_apps(task_id, app_filter)
            if len(cls.apps) == 0:
                return '找不到与该机型相关的App！'

        else :
            return model

        return cls.apps

    
class TaskPresenter(object):
    tasks = []

    @classmethod
    def get_tasks(cls):
        cls.tasks = Task.get_tasks()
        return cls.tasks


class CasePresenter(object):
    task_id = -1
    cases = []

    @classmethod
    def get_cases(cls, task_id):
        cls.task_id = task_id
        cls.cases = Case.get_cases(cls.task_id)
        return cls.cases


class PhonePresenter(object):


    @classmethod
    def get_model(cls):
        return Phone.get_phone_model()


    @classmethod
    def get_system_version(cls):
        return  Phone.get_system_version()


class RecordPresenter(object):
    """
    record_status:
        0: 未开始录制
        1：正在录制
    """
    failed_status_map = {
        2: '拖出失败!',
        3: '设备未连接!',
        4: '设备未授权!',
        5: '设备未知错误!',
        6: '只能连接1台设备!'
    }
    record_status = 0


    @classmethod
    def record(cls):
        model = Phone.get_phone_model()

        if '设备' not in model:
            cls.record_status = 1
            Record.status = 0

            thread = threading.Thread(target=Record.start_record,args=(model,))
            thread.setDaemon(True)
            thread.start()
            return True
        else :
            if '设备未连接' in model:
                Record.status = 3
            elif '设备未授权' in model:
                Record.status = 4
            else:
                Record.status = 5

            tkMessageBox.showerror('结果', model)
            return False


    @classmethod
    def finish_record(cls, app_id, app_name, platform, task_id, case_id, case_name, order):
        if Record.status != 3:
            cls.record_status = 0

            thread = threading.Thread(target=Record.finish_record,args=(app_name, platform, task_id, case_name, order))
            thread.setDaemon(True)
            thread.start()
            thread.join()

            if cls.failed_status_map.get(Record.status) is not None:
                tkMessageBox.showerror('结果', cls.failed_status_map.get(Record.status))
            else:
                key = '%s_%s_%s_%s' % (task_id, case_id, platform, app_id)
                if(ResultOrder.order_map.has_key(key)):
                    ResultOrder.order_map.pop(key)



class UploadPresenter(object):

    @classmethod
    def upload(cls):
        Upload.upload()


    @classmethod
    def get_items_to_be_uploaded(cls):
        return Upload.get_items_to_be_uploaded()


class RemakePresenter(object):


    @classmethod
    def check_remake_order(cls, task_id, app_id, platform, case_id, remake_order):
        return Remake.check_remake_order(task_id, app_id, platform, case_id, remake_order)


class VersionPresenter(object):


    @classmethod
    def get_version(cls):
        return Version.get_version()


    @classmethod
    def set_version(cls, new_version):
        Version.set_version(new_version)


class ResultOrderPresenter(object):


    @classmethod
    def hold_order(cls, task_id, case_id, platform, app_id):
        key = '%s_%s_%s_%s' % (task_id, case_id, platform, app_id)
        order = ResultOrder.order_map.get(key)

        if order is None:
            order = ResultOrder.hold_order(task_id, case_id, platform, app_id)

        return order

    @classmethod
    def get_order(cls, task_id, case_id, platform, app_id):

        return ResultOrder.get_order(task_id, case_id, platform, app_id)
