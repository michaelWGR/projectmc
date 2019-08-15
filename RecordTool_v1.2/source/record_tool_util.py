# -*- coding:utf-8 -*-
from threading import Thread
from record_tool_environment import *
import threading
import MySQLdb
import time
import json


class SqlTool(object):

    # (self, host='172.26.9.18', database='competitor_test', user='ctest_readonly', password='123456',charset='utf8'):

    # (self, host='127.0.0.1', database='temp', user='root', password='', charset='utf8'):

    def __init__(self):
        json_path = os.path.join(config_dir, 'sql.json')
        json_file = None
        try:
            json_file = open(json_path, 'r')
            data = json_file.read()
            configuration = json.loads(data)
            self.host = str(configuration['host'])
            self.database = str(configuration['database'])
            self.user = str(configuration['user'])
            self.password = str(configuration['password'])
            self.charset = str(configuration['charset'])
        except BaseException, e:
            print'无法正确获取sql连接参数,请在%s文件中重新配置!' % json_path
        finally:
            if json_file is not None:
                json_file.close()



    def __connect(self):
        self.conn = MySQLdb.Connect(host=self.host, user=self.user, passwd=self.password, db=self.database, charset=self.charset)


    def __disconnect(self):
        self.conn.close()


    def execute_query(self, sql_str, args=None):
        self.__connect()
        cursor = self.conn.cursor()
        results = cursor.fetchmany(cursor.execute(sql_str, args))
        cursor.close()
        self.__disconnect()
        return results


    def execute_update(self, sql_str, args=None):
        self.__connect()
        cursor = self.conn.cursor()
        result = cursor.execute(sql_str, args)
        self.conn.commit()
        cursor.close()
        self.__disconnect()
        return result


class UploadTool(Thread):


    def __init__(self,get_item_func,upload_func,is_daemon=False):
        threading.Thread.__init__(self)

        self.get_item_func = get_item_func
        self.upload_func = upload_func
        self.setDaemon(is_daemon)


    def run(self):
        while True:
            time.sleep(3)
            items = apply(self.get_item_func)

            for item in items:

                self.upload_func(item)

                time.sleep(1)


class JsonUtil(object):

    @classmethod
    def load_configuration(cls, dir, json_file_name):
        json_path = os.path.join(dir, json_file_name)
        json_file = None
        try:
            json_file = open(json_path, 'r')
            data = json_file.read()
            configuration = json.loads(data)
            return configuration
        except BaseException, e:
            print e
            print'无法正确获取json参数,请检查%s是否正确!' % json_path
        finally:
            if json_file is not None:
                json_file.close()

