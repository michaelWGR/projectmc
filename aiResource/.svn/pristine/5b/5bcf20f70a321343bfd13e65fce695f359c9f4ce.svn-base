# -*- coding:utf-8 -*-
import os
from enum import Enum

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ_DIR = os.path.split(BASE_DIR)[0]

# online
database = {
    "host": '172.26.9.18',
    "user": 'competitor_test',
    "password": '123456',
    "database": 'ai_test',
}

# debug
# database = {
#     "host": 'localhost',
#     "user": 'root',
#     "password": '123456',
#     "database": 'ai_test',
# }

PROCESS_TYPE = {
    'none': 0,
    'extract': 1,
    'blur10': 2,
    'blur20': 3,
    'blur30': 4,
    'blur40': 5,
    'blur50': 6,
    'mosaic5': 7,
    'mosaic10': 8,
    'mosaic15': 9,
    'mosaic20': 10,
    'colornoise50': 11,
    'colornoise100': 12,
    'colornoise150': 13,
}


class ProcessType(Enum):
    none = 0
    extract = 1
    blur10 = 2
    blur20 = 3
    blur30 = 4
    blur40 = 5
    blur50 = 6
    mosaic5 = 7
    mosaic10 = 8
    mosaic15 = 9
    mosaic20 = 10
    colornoise50 = 11
    colornoise100 = 12
    colornoise150 = 13


class GameType(Enum):
    juediqiusheng = 1
    huangyexingdong = 2
    cijizhanchang = 3
    quanjunchuji = 4
    wangzherongyao = 5