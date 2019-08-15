import MySQLdb
import shutil
import os
import time
import random
import string
import datetime
import argparse
from utils.settings import *

__script_file_path__ = os.path.dirname(__file__)
base_url = 'http://ai-resource.yypm.com/resource/'
copy_finished_file = os.path.join(__script_file_path__, "copyFileFinished.log")
copy_failed_file = os.path.join(__script_file_path__, "copyFileFailed.log")
insert_finished_file = os.path.join(__script_file_path__, "insertDataFinished.log")
insert_failed_file = os.path.join(__script_file_path__, "insertDataFailed.log")

def getDBConnection(host, db, user, passwd):
    try:
        db_conn = MySQLdb.connect(host=host,
                                  user=user,
                                  passwd=passwd,
                                  db=db,
                                  charset='utf8')
        return db_conn
    except Exception as e:
        print e


def record_exists(dbConn, table, record):
    query_string = "select count(*) from {0} where path = '{1}'".format(table, record)
    try:
        cursor = dbConn.cursor()
        cursor.execute(query_string)
        result = cursor.fetchall()
        return result[0][0] != 0
    except Exception as e:
        print e
    finally:
        cursor.close()


def insert(dbConn, table, fields, object_list):
    has_error = False
    placeholders = ["%s" for x in fields]
    assignments = ["{x} = VALUES({x})".format(x=x) for x in fields]

    query_string = """INSERT INTO
    {table}
    ({fields})
    VALUES
    ({placeholders})
    ON DUPLICATE KEY UPDATE {assignments}"""

    try:
        cursor = dbConn.cursor()
        cursor.execute(query_string.format(
            table=table,
            fields=", ".join(fields),
            placeholders=", ".join(placeholders),
            assignments=", ".join(assignments)
        ), object_list)
        dbConn.commit()
    except Exception as e:
        has_error = True
        content = "data [{0}] insert into resources table failed:{1}".format(object_list, e.message)
        wirteLog2TXT(insert_failed_file, content, True)
        dbConn.rollback()
        cursor.close()
        dbConn.close()
    return has_error


def copyOrgFile(srcFileRootPath, desFileRootPath):
    has_errors = False
    # copy failed file
    failed_list = get_failed_records(copy_failed_file)
    if failed_list:
        copy_failed_file(failed_list, desFileRootPath)
        return

    for root, dirs, files in os.walk(srcFileRootPath):
        for _file in files:
            if _file.endswith('.jpg') or _file.endswith('.png'):
                src_file_path = os.path.join(root, _file)
                dest_file_path = gen_diff_file(desFileRootPath)
                try:
                    shutil.copyfile(src_file_path, dest_file_path)
                except Exception as e:
                    has_errors = True
                    content = "Copy file [{0}] failed:{1}".format(src_file_path, e.message)
                    wirteLog2TXT(copy_failed_file, content, True)
    if not has_errors:
        wirteLog2TXT(copy_finished_file, "all copy finished without error", True)


def get_failed_records(file_path):
    object_list = []
    if not os.path.exists(file_path):
        return object_list
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            str_start = line.index('[')
            str_end = line.index(']')
            object_list.append(line[str_start + 1:str_end])
    return object_list


def copy_failed_files(failed_list_files, dest):
    has_errors = False
    for _file in failed_list_files:
        dest_file_path = gen_diff_file(dest)
        try:
            shutil.copyfile(_file, dest_file_path)
        except Exception as e:
            has_errors = True
            content = "Copy file [{0}] failed:{1}".format(_file, e.message)
            wirteLog2TXT(copy_failed_file, content, False)
    if not has_errors:
        os.remove(copy_failed_file)


def gen_diff_file(dest_dir):
    while(True):
        dest_file_name = ''.join(random.sample(string.ascii_letters + string.digits, 16)) + ".jpg"
        dest_file_path = os.path.join(dest_dir, dest_file_name)
        if not os.path.exists(dest_file_path):
            break
    return dest_file_path


def is_copy():
    if os.path.exists(copy_finished_file):
        return False
    return True


def is_insert():
    if os.path.exists(insert_finished_file):
        return False
    return True


def getObjectList(desFileRootPath):
    for root, dirs, files in os.walk(desFileRootPath):
        for _file in files:
            if _file.endswith('.jpg') or _file.endswith('.png'):
                file_path = os.path.join(root, _file)
                object_list_path = '%s%s' % (base_url, file_path[file_path.index("sample"):])
                yield object_list_path


def saveData2DB(host, db, user, passwd, desFileRootPath):
    dbConn = getDBConnection(host, db, user, passwd)
    fields = ['path', 'type', 'business_type', 'pid', 'pre_id', 'next_id', 'checked', 'process_type', 'is_leaf',
              'is_debug', 'col_int_01', 'ctime', 'mtime']
    table = 'resources'
    has_error = False
    #handling failed data
    failed_records = get_failed_records(insert_failed_file)
    if failed_records:
        for object_path in failed_records:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            object_list = (object_path, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, now_time, now_time)
            if not record_exists(dbConn, table, object_path):
                has_error = insert(dbConn, table, fields, object_list)
        if not has_error:
            os.remove(insert_failed_file)
        return

    for object_path in getObjectList(desFileRootPath):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        object_list = (object_path, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, now_time, now_time)
        if not record_exists(dbConn, table, object_path):
            has_error = insert(dbConn, table, fields, object_list)

    if not has_error:
        wirteLog2TXT(insert_finished_file, "all data inserted without error", True)


def wirteLog2TXT(file, content, is_append):
    if is_append:
        with open(file, 'a') as f:
            f.write(content)
    else:
        with open(file, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('srcFileRootPath', help='images\'s dir')
    parser.add_argument('desFileRootPath', help='output images\'s dir')
    args = parser.parse_args()
    srcFileRootPath = args.srcFileRootPath
    desFileRootPath = args.desFileRootPath
    db_host = database.get('host')
    db_name = database.get('database')
    db_user = database.get('user')
    db_pass = database.get('password')
    str_date = time.strftime("%Y%m%d", time.gmtime())
    child_path = os.path.join('sample', str_date)
    full_dest_path = os.path.join(desFileRootPath, child_path+os.sep+'adv_ocr')
    if not os.path.exists(full_dest_path):
        os.makedirs(full_dest_path)

    if is_copy():
        copyOrgFile(srcFileRootPath, full_dest_path)

    if is_insert():
        saveData2DB(db_host, db_name, db_user, db_pass, full_dest_path)
