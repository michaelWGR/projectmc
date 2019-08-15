# -*- coding: utf-8 -*-
import csv 
import requests
import os
import argparse
import sys
import MySQLdb

APP_DICT = {
    'yy': 57,
    'hy': 58,
    'yk': 59,
    'mo': 67,
    'xm': 60,
    'bg': 64,
    'lm': 73,
}

CASE_DICT = {
    'actor': {
        'cpu': 230,
        'mediaserver': 231,
        'gpu': 253,
        'flow_up': 239,
        'flow_down': 260,
        'battery_temp_start': 272,
        'battery_temp_end': 273,
        'power': 235
        
    },
    'viewer': {
        'cpu': 249,
        'mediaserver': 250,
        'gpu': 254,
        'flow_up': 261,
        'flow_down': 248,
        'battery_temp_start': 270,
        'battery_temp_end': 274,
        'power': 237,
    }
}

def upload_file(arg_suite_id, arg_file_path, arg_app, arg_case, arg_platform, arg_order,arg_client):
    db = MySQLdb.connect("172.26.9.18","competitor_test","123456","competitor_test" )
    cursor = db.cursor()
    sql = "select id from results where suite_id = %s and case_id = %s and app_id = %s and platform = '%s' and value_order = %s" % (arg_suite_id, CASE_DICT.get(arg_client,{}).get(arg_case, -1), APP_DICT.get(arg_app,-1), arg_platform, arg_order)
    # url = 'http://results.yypm.com/management/suite/' + arg_suite_id + '/result/upload_source'
    url = 'http://results.yypm.com/management/result/grid/' + arg_suite_id + '/upload.json'
    datas = {
        'app_id': APP_DICT.get(arg_app,None),
        'case_id': CASE_DICT.get(arg_client,{}).get(arg_case, None),
        'platform': arg_platform,
        'suite_id': arg_suite_id,
        'value_order': arg_order,
    }
    # datas = {}
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) != 0:
            print 'next'
            cursor.close()
            db.close()
            return
            datas['result_id'] = data[0][0]
    except Exception, e:
        print e
    # print datas
    cursor.close()
    db.close()
    # return 
    if datas['case_id'] is None:
        print arg_file_path
        print arg_case
        print datas
        return
    datas = {}
    response = requests.post(url=url,data=datas, files={'source_file':open(arg_file_path, 'rb')});
    text = response.json()
    if text.get('code') == 0:
        print 'upload success'
        save_data(arg_suite_id, arg_app, arg_case, arg_platform, arg_order, arg_client, '0' , text.get('result').get('path'))
    else:
        print 'upload fail'

    

def save_data(arg_suite_id, arg_app,arg_case,arg_platform,arg_order,arg_client,arg_value,arg_sourcefile=None):
    db = MySQLdb.connect("172.26.9.18","competitor_test","123456","competitor_test" )
    cursor = db.cursor()
    sql = "select id from results where suite_id = %s and case_id = %s and app_id = %s and platform = '%s' and value_order = %s" % (arg_suite_id, CASE_DICT.get(arg_client,{}).get(arg_case, -1), APP_DICT.get(arg_app,-1), arg_platform, arg_order)
    # url = 'http://results.yypm.com/management/result/save'
    url = 'http://results.yypm.com/management/result/grid/' + arg_suite_id + '/save.json'
    datas = {
        'app_id': APP_DICT.get(arg_app,None),
        'case_id': CASE_DICT.get(arg_client,{}).get(arg_case, None),
        'platform': arg_platform,
        'suite_id': arg_suite_id,
        'value_order': arg_order,
        'value':arg_value,
        'source_file':arg_sourcefile
    }
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) != 0:
            print 'next'
            cursor.close()
            db.close()
            return
            datas['result_id'] = data[0][0]
    except Exception, e:
        print e
    # print datas
    cursor.close()
    db.close()
    # return
    if datas['case_id'] is None:
        print arg_case
        print datas
        return
    
    response = requests.post(url=url,data=datas);
    text = response.json()
    if text.get('code') == 0:
        print 'success'
    else:
        print 'fail'
    
    

def main():
    argparser = argparse.ArgumentParser("自动提交android的评测数据，输入性能文件所在的目录，以及suite_id，会自动检测app，case进行提交，不会重复提交数据。注意事项：该脚本hardcode了caseid等信息")
    argparser.add_argument('base_path')
    argparser.add_argument('suite_id')
    args = argparser.parse_args()
    base_path = args.base_path
    suite_id = args.suite_id

    for root, dirs, files in os.walk(base_path):
        for _file in files:
            if not _file.startswith('.') and _file.endswith('.csv'):
                items =  _file[:-4].split('_')
                dict_ = {'app': items[0],'client': items[1],'order': items[2],'item': items[3],'platform': 'android'}
                file_path = os.path.join(root,_file)
                if dict_.get('item') == 'network':
                    upload_file(suite_id, file_path, dict_.get('app'), 'flow_up', dict_.get('platform'), dict_.get('order'), dict_.get('client'))
                    upload_file(suite_id, file_path, dict_.get('app'), 'flow_down', dict_.get('platform'), dict_.get('order'), dict_.get('client'))
                elif dict_.get('item') == 'battery':
                    battery = {
                        'temp_start': -1,
                        'temp_end': -1,
                        'power_end': -1
                    }
                    with open(file_path, 'rb') as battery_file:
                        reader = csv.reader(battery_file)
                        for row in reader:
                            if battery['temp_start'] == -1:
                                battery['temp_start'] = row[1]
                            else:
                                battery['temp_end'] = row[1]
                                battery['power_end'] = row[2]
                        save_data(suite_id, dict_.get('app'),'battery_temp_start',dict_.get('platform'),dict_.get('order'),  dict_.get('client'), battery['temp_start'])
                        save_data(suite_id, dict_.get('app'),'battery_temp_end',dict_.get('platform'),dict_.get('order'),  dict_.get('client'), battery['temp_end'])
                        save_data(suite_id, dict_.get('app'),'power',dict_.get('platform'),dict_.get('order'),  dict_.get('client'), battery['power_end'])
                else:
                    upload_file(suite_id, file_path, dict_.get('app'),dict_.get('item'),dict_.get('platform'),dict_.get('order'),  dict_.get('client'))
if __name__ == '__main__':
    main()

