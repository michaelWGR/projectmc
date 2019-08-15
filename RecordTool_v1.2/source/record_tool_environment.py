# -*- coding:utf-8 -*-
import os
import platform

#获取操作系统类型
operate_system = platform.system()

# 当前目录路径
cur_dir = os.path.abspath(os.path.dirname(os.sys.argv[0]))

# 父目录路径
par_dir = os.path.dirname(cur_dir)

# configurations目录路径
config_dir = os.path.join(par_dir, 'configurations')
if not os.path.exists(config_dir):
    os.mkdir(config_dir)

#data目录路径
data_dir = os.path.join(par_dir, 'data')
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

#bin目录路径
bin_dir = os.path.join(par_dir, 'bin')
if not os.path.exists(bin_dir):
    os.mkdir(bin_dir)

#source目录路径
src_dir = os.path.join(par_dir, 'source')
if not os.path.exists(src_dir):
    os.mkdir(src_dir)

#backup目录路径
bkp_dir = os.path.join(par_dir, 'bin-backup')
if not os.path.exists(bkp_dir):
    os.mkdir(bkp_dir)
