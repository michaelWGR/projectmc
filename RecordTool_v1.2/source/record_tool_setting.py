# -*- coding:utf-8 -*-

#录制参数,按机型或系统配置
record_args = [
    {'model':'HUAWEI P7-L00','args':'--bit-rate 16000000 --size 720x1080'},
    {'system':'5.1.1','args': '--bit-rate 16000000 --size 720x1080'},
    {'model':'HUAWEI P7-L00','system':'5.1.1','args':'--bit-rate 16000000 --size 720x1080'}
]

#默认的录制参数，如果当前机型无法获取record_args中的参数，则采用此参数
default_record_args = '--bit-rate 16000000'


#部分机器的型号显示不正常，需人工配置机型命名映射
model_name_map={
    '2013023': 'HM 1W'
}

#机型和app的映射
model_app_map = {
    'SM-G9350': '三星 s7',
    'OPPO R9s': 'oppo r9s',
    'HUAWEI P7-L00': '华为 p7',
    'OPPO R11': 'oppo r11',
    'SM-G9500': '三星 s8',
    'vivo X9i': 'vivo x9i',
    'NX511J': '努比亚 z9 mini',
    'M355': '魅族 mx3',
    'Coolpad 8297': '酷派 大神f1',
    'OPPO A37m': 'oppo a37',
    'HUAWEI G750-T00': '华为 3x',
    'HM 1W': '红米 1w',
    'OPPO A59s': 'oppo a59s',
    'Mi Note 3': '小米 note3',
    'HM NOTE 1TD': '红米 note1'

}
