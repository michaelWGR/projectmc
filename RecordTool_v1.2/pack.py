# -*- coding:utf-8 -*-
from subprocess import Popen
from subprocess import PIPE
import os
import json
import sys
import shutil
import datetime
import platform


#打包脚本
def pack():

    #获取当前操作系统类型
    operate_system = platform.system()

    #获取当前目录
    cur_dir = os.path.abspath(os.path.dirname(os.sys.argv[0]))

    #bin目录路径
    bin_dir = os.path.join(cur_dir,'bin')
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)
    #configurations目录路径
    config_dir = os.path.join(cur_dir,'configurations')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    #source目录路径
    src_dir = os.path.join(cur_dir, 'source')
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)
    #bin-backup目录路径
    bkp_dir = os.path.join(cur_dir, 'bin-backup')
    if not os.path.exists(bkp_dir):
        os.mkdir(bkp_dir)

    #获取版本配置参数
    json_file = None
    json_path = os.path.join(config_dir, 'version.json')
    try:
        json_file = open(json_path, 'r')
        version_info = json_file.read()
        version = json.loads(version_info)['version']
    except BaseException, e:
        print'无法正确获取版本号,请检查%s文件!' % json_path
        sys.exit()
    finally:
        if json_file is not None:
            json_file.close()

    print '打包中.....'
    print '正在打包的录制工具版本为%s，如有误，请检查%s文件的配置' %(version, json_path)
    #打包命令
    command = 'pyinstaller -F %s' % 'record_tool_view.py'
    sub = Popen(command.split(), stdout=PIPE, stderr=PIPE, cwd=src_dir)
    stdout, stderr = sub.communicate()
    print stdout
    print stderr

    # 打包会在源码目录产生dist和build两个文件夹,生成的可执行文件位于dist目录下
    dist_dir = os.path.join(src_dir, 'dist')
    build_dir = os.path.join(src_dir, 'build')

    #stderr的输出信息中包含'completed successfully'意味打包成功
    if 'completed successfully' in stderr:
        try:

            # 将可执行文件从dist文件夹移动到bin目录下，并重命名
            if 'Darwin' in operate_system:
                tool_path = os.path.join(bin_dir, 'Recorder_Mac')
                shutil.copy(os.path.join(dist_dir, 'record_tool_view'), tool_path)
            elif 'Windows' in operate_system:
                tool_path = os.path.join(bin_dir, 'Recorder_Win.exe')
                shutil.copy(os.path.join(dist_dir, 'record_tool_view.exe'), tool_path)

            #备份一份到bin-backup目录
            ctime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            temp = version.split('.')
            if not os.path.exists(bkp_dir):
                os.mkdir(bkp_dir)
            if 'Darwin' in operate_system:
                backup_file = os.path.join(bkp_dir, 'Recorder_Mac_V%s_%s_%s' %(temp[0], temp[1], ctime))
            elif 'Windows' in operate_system:
                backup_file = os.path.join(bkp_dir, 'Recorder_Win_V%s_%s_%s.exe' %(temp[0], temp[1], ctime))
            shutil.copy(tool_path, backup_file)

        except IOError, e:
            print e
            print '打包失败!'
    else :
        print '打包失败'

    # 删除打包生成的dist、build目录以及spec文件
    shutil.rmtree(dist_dir)
    shutil.rmtree(build_dir)
    os.remove(os.path.join(src_dir, 'record_tool_view.spec'))


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    pack()
