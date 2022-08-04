# -*- coding:utf-8 -*-
import sys
import os
import datetime
import argparse
import random
import string
import Queue
import traceback
from shutil import copyfile

from .utils.settings import *
import django
from django.db import transaction

sys.path.append(PROJ_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'aiResource.settings'
django.setup()

from management.models import Resource

LEGAL_EXT = ('.png', '.jpg', 'jpeg', '.bmp')

"""
由于 path重名检查效率极低
所以仅保证每一次入库的图片不重名
不同天执行url不会重复

本脚本仅允许每天执行一次
"""


class ImageMeta(object):
    def __init__(self, image_path, output_disk):
        self.image_path = os.path.abspath(image_path)
        self.output_disk = output_disk
        self.image_dir = os.path.dirname(image_path)
        self.image_name = os.path.basename(image_path)
        self.location = self.image_name.rfind('.')
        self.image_name_noext = self.image_name[:self.location]
        self.image_new_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        self.image_path_format = 'sample/{datetime}/ad_ocr/{image_name}'.format(
            datetime=datetime.datetime.now().strftime('%Y%m%d'),
            image_name=self.image_new_name + self.image_name[self.location:])

        self.image_output_path = os.path.join(self.output_disk, self.image_path_format)
        self.image_output_dir = os.path.dirname(self.image_output_path)
        self.image_output_url = 'http://ai-resource.yypm.com/resource/' + self.image_path_format
        self.mata_file_path = os.path.join(self.image_dir, '.' + self.image_name_noext + '.meta')  # 存储图片归档后的url

    def random_image_name(self):
        self.image_new_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        self.image_path_format = 'sample/{datetime}/ad_ocr/{image_name}'.format(
            datetime=datetime.datetime.now().strftime('%Y%m%d'),
            image_name=self.image_new_name + self.image_name[self.location:])
        self.image_output_path = os.path.join(self.output_disk, self.image_path_format)
        self.image_output_dir = os.path.dirname(self.image_output_path)
        self.image_output_url = 'http://ai-resource.yypm.com/resource/' + self.image_path_format


def get_new_record(image_url, business_type):
    return Resource(path=image_url, type=1, business_type=business_type, process_type=0, pid=0, pre_id=0, next_id=0,
                    is_leaf=1,
                    checked=0, col_int_01=0, is_debug=0)


def get_all_ids():
    ids = []
    results = Resource.objects.filter(process_type=0,business_type=1,is_debug=0).order_by('id').values_list('id', flat=True)
    for id_ in results:
        ids.append(id_)
    return ids


def is_exist(image_url):
    # return os.path.exists(new_image_path)
    return Resource.objects.filter(path=image_url).count() > 0


def warehousing_image(image_meta, business_type,id):
    transaction.set_autocommit(False)
    try:

        # chech is file exist in database
        # while is_exist(image_meta.image_output_dir):
        #     image_meta.random_image_name()

        # move file

        if not os.path.exists(image_meta.image_output_dir):
            os.makedirs(image_meta.image_output_dir)

        copyfile(image_meta.image_path, image_meta.image_output_path)
        if id is None:
            resource = get_new_record(image_meta.image_output_url, business_type)
            resource.save()
        else:
            Resource.objects.filter(id=id).update(path=image_meta.image_output_url)
        with open(image_meta.mata_file_path, 'wb') as meta_f:
            meta_f.write(image_meta.image_output_url)
        transaction.commit()
    except Exception:
        transaction.rollback()
        if os.path.exists(image_meta.image_output_path):
            os.remove(image_meta.image_output_path)
        if os.path.exists(image_meta.mata_file_path):
            os.remove(image_meta.mata_file_path)
        print(traceback.format_exc())


def insert_or_ignore(image_meta, business_type):
    line = None
    with open(image_meta.mata_file_path, 'rb') as r_f:
        line = r_f.readline()
    if not is_exist(line):
        resource = get_new_record(line, business_type)
        resource.save()

    image_new_path = os.path.join(image_meta.output_disk, line.replace('http://ai-resource.yypm.com/resource/', ''))
    if not os.path.exists(image_new_path):
        if not os.path.exists(image_meta.image_output_dir):
            os.makedirs(image_meta.image_output_dir)
        copyfile(image_meta.image_path, image_new_path)


def main():
    argparser = argparse.ArgumentParser('warehousing image.!!! do not run in same day twice')
    argparser.add_argument('src_sample_dir')
    argparser.add_argument('target_dir')
    argparser.add_argument('--business_type', help='0: pron, 1: ad-OCR, 2: game-OCR', choices=[0, 1, 2], type=int,
                           default=1)
    args = argparser.parse_args()

    sample_dir = args.src_sample_dir
    target_dir = args.target_dir
    business_type = args.business_type

    url_list = []
    image_queue = Queue.Queue()
    # collect warehousing image
    for root, dirs, files in os.walk(sample_dir):
        for file_ in files:
            # print file_
            if file_.lower().endswith(LEGAL_EXT):
                image_queue.put(ImageMeta(os.path.join(root, file_), target_dir))

    ids = get_all_ids()
    while image_queue.qsize() > 0:
        # print image_queue.qsize()
        image_meta = image_queue.get()
        while image_meta.image_output_url in url_list:
            image_meta.random_image_name()
        url_list.append(image_meta.image_output_url)
        if not os.path.exists(image_meta.image_path) or not os.path.isfile(image_meta.image_path):
            continue
        if not os.path.exists(image_meta.mata_file_path):
            if len(ids) > 0:
                id_ = ids.pop(0)
                warehousing_image(image_meta, business_type, id_)
            else:
                warehousing_image(image_meta, business_type, None)
        else:  # check if had save
            insert_or_ignore(image_meta, business_type)


def clean_meta(iamge_dir):
    for root,dirs,files in os.walk(iamge_dir):
        for file_ in files:
            if file_.endswith('.meta'):
                os.remove(os.path.join(root, file_))


if __name__ == '__main__':
    main()
    # path = ''
    # clean_meta(path)

    # location = 'dsadsa.dsdsafdsf.jpg'.rfind('.')
    # print 'dsadsa.dsdsafdsf.jpg'[:location]
    # print 'dsadsa.dsdsafdsf.jpg'[location + 1:]
    # # print ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
    # print [].pop(0)
