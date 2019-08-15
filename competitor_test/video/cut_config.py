# -*- coding:utf-8 -*-

CONFIG = {
    # Android
    'yy_android': {
        'pre_roi': {'x': 0, 'y': 2, 'width': 960, 'height': 539},
        'resize': {'width': 1920, 'height': 1079}
    },
    'yy_android_source': {
        'pre_roi': {'x': None, 'y': None, 'width': 1920, 'height': 1079}
    },
    'hy_android': {
        'pre_roi': {'x': 5, 'y': 0, 'width': 853, 'height': 480},
        'resize': {'width': 1920, 'height': 1080}
    },
    'hy_android_source': {},
    # 'cs_android': {
    #     'pre_roi': {'x': 5, 'y': 0, 'width': 852, 'height': 480},
    #     'resize': {'width': 1918, 'height': 1080},
    #     'roi': {'x': 0, 'y': 140, 'width': 1918, 'height': 940}
    # },
    # 'cs_android_source': {
    #     'roi': {'x': 0, 'y': 140, 'width': 1918, 'height': 940}
    # },
    'cs_android': {
        'pre_roi': {'x': 5, 'y': 0, 'width': 852, 'height': 480},
        'resize': {'width': 1918, 'height': 1080},
        'roi': {'x': 0, 'y': 163, 'width': 1918, 'height': 917}
    },
    'cs_android_source': {
        'roi': {'x': 0, 'y': 163, 'width': 1918, 'height': 917}
    },
    '720P': {
        'resize': {'width': 720, 'height': 1280},
        'roi': {'x': 0, 'y': 142, 'width': 720, 'height': 864}
    },
    '720P_source': {
        'roi': {'x': 0, 'y': 142, 'width': 720, 'height': 864}
    },
    '1080P': {
        'resize': {'width': 1080, 'height': 1920},
        'roi': {'x': 0, 'y': 212, 'width': 1080, 'height': 1270}
    },
    '1080P_source': {
        'roi': {'x': 0, 'y': 212, 'width': 1080, 'height': 1270}
    },
    # iOS
    'yy_ios': {
        'resize': {'width': 1920, 'height': 1080},
        'roi': {'x': 0, 'y': 160, 'width': 1919, 'height': 918}
    },
    'yy_ios_source': {
        'roi': {'x': 0, 'y': 160, 'width': 1919, 'height': 918}
    },
    'hy_ios': {
        'resize': {'width': 1920, 'height': 1080},
        'roi': {'x': 0, 'y': 160, 'width': 1919, 'height': 918}
    },
    'hy_ios_source': {
        'roi': {'x': 0, 'y': 160, 'width': 1919, 'height': 918}
    },
    'cs_ios': {
        'pre_roi': {'x': 0, 'y': 1, 'width': 853, 'height': 479},
        'resize': {'width': 1919, 'height': 1078},
        'roi': {'x': 0, 'y': 160, 'width': 1919, 'height': 918}
    },
    'cs_ios_source': {
        'roi': {'x': 0, 'y': 160, 'width': 1919, 'height': 918}
    },
}