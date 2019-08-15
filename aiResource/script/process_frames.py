# -*- coding:utf-8 -*-

import os
import argparse
import cv2
import MySQLdb
import datetime
import threading
import csv
import Queue
import numpy as np
import multiprocessing as mp
import traceback
from multiprocessing import Pool
from shutil import copyfile

# from aiResource.settings import PROCESS_TYPE
from utils.settings import *


class Processor(object):
    def __init__(self):
        pass

    @staticmethod
    def can_process(process_type):
        return False

    def process(self, frame):
        return frame


class BlurProcessor(Processor):
    def __init__(self, process_argument):
        super(BlurProcessor, self).__init__()
        self.argument = None
        self.process_arguments = {
            'blur10': (10, 10),
            'blur20': (20, 20),
            'blur30': (30, 30),
            'blur40': (40, 40),
            'blur50': (50, 50),
            # 'blur10': (5, 5),
            # 'blur20': (10, 10),
            # 'blur30': (15, 15),
            # 'blur40': (20, 20),
            # 'blur50': (25, 25),
        }
        self.argument = self.process_arguments.get(process_argument, None)
        if not self.argument:
            raise RuntimeError('argument is None')

    @staticmethod
    def can_process(process_type):
        can_process_type = [
            'blur10',
            'blur20',
            'blur30',
            'blur40',
            'blur50',
        ]
        if process_type in can_process_type:
            return True
        return False

    def process(self, frame):
        tmp_frame = np.copy(frame)
        return cv2.blur(tmp_frame, self.argument)


class ColorNoiseProcessor(Processor):
    def __init__(self, process_argument):
        super(ColorNoiseProcessor, self).__init__()
        self.process_arguments = {
            'colornoise50': 50,
            'colornoise100': 100,
            'colornoise150': 150
        }
        self.argument = self.process_arguments.get(process_argument, None)
        if not self.argument:
            raise RuntimeError('argument is None')

    @staticmethod
    def can_process(process_type):
        can_process_type = [
            'colornoise50',
            'colornoise100',
            'colornoise150'
        ]
        if process_type in can_process_type:
            return True
        return False

    def process(self, frame):
        tmp_frame = np.copy(frame)
        mean = 0.0
        r = np.random.normal(mean, self.argument, tmp_frame.shape)
        noisy_img = tmp_frame + r
        noisy_img_clipped = np.clip(noisy_img, 0, 255)
        return noisy_img_clipped


class MosaicsProcessor(Processor):
    def __init__(self, process_argument):
        super(MosaicsProcessor, self).__init__()
        self.process_arguments = {
            'mosaic5': 5,
            'mosaic10': 10,
            'mosaic15': 15,
            'mosaic20': 20,
        }
        self.argument = self.process_arguments.get(process_argument, None)
        if not self.argument:
            raise RuntimeError('argument is None')

    @staticmethod
    def can_process(process_type):
        can_process_type = [
            'mosaic5',
            'mosaic10',
            'mosaic15',
            'mosaic20',
        ]
        if process_type in can_process_type:
            return True
        return False

    def process(self, frame):
        tmp_frame = np.copy(frame)
        (height, width, depth) = tmp_frame.shape
        for y in range(0, height, self.argument):
            for x in range(0, width, self.argument):
                tmp_frame[y:y + self.argument, x:x + self.argument] = tmp_frame[y, x]
        return tmp_frame


ready_processors = {
    'blur10': BlurProcessor('blur10'),
    'blur20': BlurProcessor('blur20'),
    'blur30': BlurProcessor('blur30'),
    'blur40': BlurProcessor('blur40'),
    'blur50': BlurProcessor('blur50'),
    'mosaic5': MosaicsProcessor('mosaic5'),
    'mosaic10': MosaicsProcessor('mosaic10'),
    'mosaic15': MosaicsProcessor('mosaic15'),
    'mosaic20': MosaicsProcessor('mosaic20'),
    'colornoise50': ColorNoiseProcessor('colornoise50'),
    'colornoise100': ColorNoiseProcessor('colornoise100'),
    'colornoise150': ColorNoiseProcessor('colornoise150'),
}


def get_process_image(coon, last_id, business_type, process_type):
    # todo：需要优化，数据过多会有问题

    images = Queue.Queue()
    # coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
    #                        database.get('database'), charset='utf8')
    # only process pron business_type image
    get_all_frames_sql = 'select id,path,business_type,value from resources where process_type = %s and business_type = %s and id > %s and is_debug = 0 ORDER by id limit 1000'  # get all extract image
    cursor = coon.cursor()

    cursor.execute(get_all_frames_sql, (process_type, business_type, last_id,))
    rows = cursor.fetchall()
    for row in rows:
        id = row[0]
        path = os.path.join(row[1].strip().replace('http://ai-resource.yypm.com/resource/', ''))
        business_type = row[2]
        value = row[3]
        images.put((id, path, business_type, value))

    # coon.close()
    return images


def is_had_deal(coon, frame_item, process_type):
    check_sql = 'select count(*) from resources where pid = %s and process_type = %s'
    cursor = coon.cursor()
    cursor.execute(check_sql, (frame_item[0], process_type,))
    resutls = cursor.fetchall()
    if resutls[0][0] >= 1:
        return True
    return False


def save_to_database(coon, frame_item, deal_save_path, process_type):
    update_sql = 'update resources set is_leaf = 0 where id = %s'
    insert_sql = 'insert into resources(path,type,business_type,pid,next_id,pre_id,process_type,value, checked,is_leaf,is_debug,col_int_01,ctime,mtime) values (' \
                 '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor = coon.cursor()
    is_debug = 0
    col_int_01 = 0
    try:
        cursor.execute(update_sql, (frame_item[0],))
        path = 'http://ai-resource.yypm.com/resource/' + deal_save_path
        type = 1
        business_type = int(frame_item[2])
        pid = int(frame_item[0])
        next_id = 0
        pre_id = 0
        process_type = int(PROCESS_TYPE.get(process_type))
        checked = 0
        is_leaf = 1
        value = frame_item[3]
        ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mtime = ctime
        cursor.execute(insert_sql, (
            path, type, business_type, pid, next_id, pre_id, process_type, value, checked, is_leaf, is_debug,
            col_int_01, ctime, mtime,))
        coon.commit()
    except Exception, e:
        print e
        coon.rollback()


def frame_process(image, keys, sample_dir, deal_sample_disk, deal_image_dir_format, deal_image_path_format):
    coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
                           database.get('database'), charset='utf8')

    source_path = os.path.join(sample_dir, image[1])
    frame = cv2.imread(source_path)
    for process_type in keys:

        tmp_frame = frame
        processor = ready_processors.get(process_type, None)

        if not processor:
            raise RuntimeError('no target processor')

        image_paths = image[1].split('/')[-2:]
        deal_image_dir = deal_image_dir_format.format(process_type=process_type,
                                                      datetime=datetime.datetime.now().strftime('%Y%m%d'),
                                                      video_name=image_paths[0])
        deal_image_formatten = deal_image_path_format.format(process_type=process_type,
                                                             datetime=datetime.datetime.now().strftime(
                                                                 '%Y%m%d'),
                                                             video_name=image_paths[0],
                                                             image_name=image_paths[1])

        deal_path = os.path.join(deal_sample_disk, deal_image_formatten)
        if not os.path.exists(source_path):
            raise RuntimeError()

        if not os.path.exists(deal_image_dir):
            os.makedirs(deal_image_dir)
        if is_had_deal(coon, image, int(PROCESS_TYPE.get(process_type))):
            continue

        after_deal = processor.process(tmp_frame)
        cv2.imwrite(deal_path, after_deal)
        save_to_database(coon, image, deal_image_formatten, process_type)


def copy_read_error_image(src_image, error_path):
    """
    copy无法读取图片到指定目录
    :return:
    """
    new_dir = os.path.dirname(error_path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    copyfile(src_image, error_path)


def update_processed_image():
    """
    由于发现有图片的处理处理有问题，需要重新处理
    :return:
    """

    argparser = argparse.ArgumentParser('reprocess single processor processed image')
    argparser.add_argument('sample_dir', help="sample dir")
    argparser.add_argument('deal_sample_dir', help="deal sample dir")
    argparser.add_argument('start_id', help="source image start id", type=int, default=0)
    argparser.add_argument('end_id', help="source image end id")
    argparser.add_argument('process_types', nargs="+", choices=['blur10', 'blur20', 'blur30', 'blur40', 'blur50',
                                                                'mosaic5', 'mosaic10', 'mosaic15', 'mosaic20',
                                                                'colornoise50', 'colornoise100', 'colornoise150'])
    args = argparser.parse_args()
    sample_dir = args.sample_dir
    deal_sample_dir = args.deal_sample_dir
    start_id = args.start_id
    end_id = args.end_id
    process_types = args.process_types

    def get_process_image_inner(coon, last_id, end_id):
        images = Queue.Queue()
        # coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
        #                        database.get('database'), charset='utf8')
        # only process pron business_type image
        get_all_frames_sql = 'select id,path from resources where type = 1 and business_type = 0 and process_type = 1 and id >= %s and id <= %s ORDER by id limit 1000'  # get all extract image
        # get_all_frames_sql = 'select id,path from resources where type = 1 and business_type = 0 and process_type = 1 and id > %s and id <= 10 ORDER by id limit 1000'  # get all extract image
        cursor = coon.cursor()

        cursor.execute(get_all_frames_sql, (last_id, end_id))
        rows = cursor.fetchall()
        for row in rows:
            id = row[0]
            path = row[1].strip().replace('http://ai-resource.yypm.com/resource/', '')
            images.put((id, path))

        # coon.close()
        # print cursor._last_executed
        return images

    def process_image_inner(coon, image_item, process_type_enum, sample_dir, deal_sample_dir):
        src_id = image_item[0]
        src_path_rela = image_item[1]
        cursor = coon.cursor()
        try:
            cursor.execute('select id,path from resources where process_type = %s and pid = %s',
                           (process_type_enum, src_id))
            dst_row = cursor.fetchone()

            if dst_row:
                dst_id = dst_row[0]
                dst_path_rela = dst_row[1].strip().replace('http://ai-resource.yypm.com/resource/', '')

                src_path_abs = os.path.join(sample_dir, src_path_rela)
                dst_path_abs = os.path.join(deal_sample_dir, dst_path_rela)
                dst_path_abs_dir = os.path.dirname(dst_path_abs)
                if not os.path.exists(src_path_abs):
                    raise RuntimeError("target file not exist %s" % (src_path_abs,))
                if not os.path.exists(dst_path_abs_dir):
                    os.makedirs(dst_path_abs_dir)

                processor = ready_processors.get(process_type)
                frame = cv2.imread(src_path_abs)
                new_frame = processor.process(frame)
                cv2.imwrite(dst_path_abs, new_frame)
        except Exception, e:
            print traceback.format_exc()
            print cursor._last_executed
        finally:
            cursor.close()

    coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
                           database.get('database'), charset='utf8')

    for process_type in process_types:

        process_type_enum = PROCESS_TYPE.get(process_type)
        last_id = start_id
        image_queue = get_process_image_inner(coon, last_id, end_id)
        # print image_queue.qsize()

        while image_queue.qsize() > 0:
            last_start_time = datetime.datetime.now()
            while image_queue.qsize() > 0:
                image_item = image_queue.get()
                last_id = image_item[0]
                process_image_inner(coon, image_item, process_type_enum, sample_dir, deal_sample_dir)

            image_queue = get_process_image_inner(coon, last_id, end_id)
            now_time = datetime.datetime.now()
            print 'last 1000 image process time : %s' % (now_time - last_start_time)
            print 'id before %s had reprocess' % (last_id,)


def check_is_processed():
    argparser = argparse.ArgumentParser("check is all process image finished")
    argparser.add_argument("--business_type", help="0: pron, 1: ad-OCR, 2: game-OCR", type=int, default=0)
    argparser.add_argument("src_dir", help="source sample dir,such as: I:\\sample input: I:\\")
    argparser.add_argument("processed_dir", help="processsed sample dir,such as: I:\\deal_sample input: I:\\")
    args = argparser.parse_args()

    src_dir = args.src_dir
    processed_dir = args.processed_dir

    def get_process_date(coon, start_id, business_type):
        images = Queue.Queue()
        cursor = coon.cursor()
        try:
            # get_all_frames_sql = 'select id,path from resources where type = 1 and business_type = %s and process_type > 1 and id >= %s and is_debug = 0 ORDER by id limit 1000'  # get all extract image
            get_all_frames_sql = "select res1.id,res2.path,res1.path,res1.process_type from resources as res1 left JOIN resources as res2 on (res1.pid = res2.id) where res1.type = 1 and res1.business_type = %s and res1.process_type > 1 and res1.id >= %s and res1.is_debug = 0 ORDER BY res1.id limit 1000"

            cursor.execute(get_all_frames_sql, (business_type, start_id,))
            rows = cursor.fetchall()
            for row in rows:
                id = row[0]
                p_path = row[1].strip().replace('http://ai-resource.yypm.com/resource/', '')
                c_path = row[2].strip().replace('http://ai-resource.yypm.com/resource/', '')
                process_type = row[3]
                images.put((id, p_path, c_path, process_type))
            return images
        except Exception,e:
            print traceback.format_exc()
            print cursor._last_executed
            raise RuntimeError(e)
        finally:
            return images

    coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
                           database.get('database'), charset='utf8')

    start_id = 0
    images = get_process_date(coon, start_id, args.business_type)
    count = 1
    fixed = 0
    while images.qsize() > 0:
        start_time = datetime.datetime.now()
        while images.qsize() > 0:
            image = images.get()
            start_id = image[0]
            src_path = os.path.join(src_dir, image[1])
            process_path = os.path.join(processed_dir, image[2])
            error_path = os.path.join(processed_dir, image[2]).replace('sample', 'fixerror_sample')
            process_dir = os.path.dirname(process_path)
            if not os.path.exists(process_path):
                processor = ready_processors.get(ProcessType(image[3]).name, None)
                if not processor:
                    raise RuntimeError('no Process found')
                frame = cv2.imread(src_path)
                if frame is None:
                    copy_read_error_image(src_path, error_path)
                new_frame = processor.process(frame)
                if not os.path.exists(process_dir):
                    os.makedirs(process_dir)
                cv2.imwrite(process_path, new_frame)
                fixed += 1

        print "1000 image had checked ,spent time %s" % (datetime.datetime.now() - start_time)
        print "%s image had processed. " % (1000 * count)
        print "id less than %s had checked" % (start_id,)
        print "fixed %s " % (fixed,)
        images = get_process_date(coon, start_id, args.business_type)
        count += 1


def main():
    argparser = argparse.ArgumentParser('process all image resource')
    # subparsers = argparser.add_subparsers()
    # normal_model = subparsers.add_parser('as_normal', help="normal model")
    # normal_model.add_argument('sample_dir', help='source image dir')
    # normal_model.add_argument('deal_sample_disk', help='save image dir')
    # normal_model.add_argument('--business_type', help="0 pron, 1 ad-OCR, 2:game-OCR", choices=[0, 1, 2], type=int, default=0)
    # normal_model.add_argument('--target_process_type', help="0 null, 1 extract", choices=[0, 1], type=int, default=1)
    # normal_model.add_argument('process_types', nargs="+", help='blur10,blur20,blur30,blur40,blur50',
    #                        choices=['blur10', 'blur20', 'blur30', 'blur40', 'blur50',
    #                                 'mosaic5', 'mosaic10', 'mosaic15', 'mosaic20',
    #                                 'colornoise50', 'colornoise100', 'colornoise150'])
    # rerun_model = subparsers.add_parser('rerun', help='rerun process image, save ')
    argparser.add_argument('sample_dir', help='source image dir')
    argparser.add_argument('deal_sample_disk', help='save image dir')
    argparser.add_argument('--business_type', help="0 pron, 1 ad-OCR, 2:game-OCR", choices=[0, 1, 2], type=int, default=0)
    argparser.add_argument('--target_process_type', help="0 null, 1 extract", choices=[0, 1], type=int, default=1)
    argparser.add_argument('process_types', nargs="+", help='blur10,blur20,blur30,blur40,blur50',
                           choices=['blur10', 'blur20', 'blur30', 'blur40', 'blur50',
                                    'mosaic5', 'mosaic10', 'mosaic15', 'mosaic20',
                                    'colornoise50', 'colornoise100', 'colornoise150'])
    args = argparser.parse_args()

    sample_dir = args.sample_dir
    deal_sample_disk = args.deal_sample_disk
    process_types = args.process_types
    business_type = args.business_type
    target_process_type = args.target_process_type

    deal_image_dir_format = 'deal_sample/{process_type}/{datetime}/{video_name}'
    deal_image_path_format = 'deal_sample/{process_type}/{datetime}/{video_name}/{image_name}'

    coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
                           database.get('database'), charset='utf8')
    keys = process_types
    keys = sorted(keys)

    memoryerror_image_list = []

    try:
        last_id = 0
        images = get_process_image(coon, last_id, business_type, target_process_type)
        # while images.qsize() > 0:
        # 	image = images.get()
        # 	print image[1]
        while images.qsize() > 0:
            # print 0
            last_start_time = datetime.datetime.now()
            while images.qsize() > 0:
                image = images.get()
                
                last_id = int(image[0])
                source_path = os.path.join(sample_dir, image[1])
                error_path = os.path.join(sample_dir, 'error_sample', image[1])
                frame = cv2.imread(source_path)
                if frame is None:  # 读图error就先copy图片到指定目录以便进行后处理
                    copy_read_error_image(source_path, error_path)
                    continue
                for process_type in keys:
                    processor = ready_processors.get(process_type, None)
                    if not processor:
                        raise RuntimeError('no target processor')

                    image_paths = image[1].split('/')[-3:]
                    deal_image_dir = deal_image_dir_format.format(process_type=process_type,
                                                                  datetime=image_paths[0],
                                                                  video_name=image_paths[1])
                    deal_image_formatten = deal_image_path_format.format(process_type=process_type,
                                                                         datetime=image_paths[0],
                                                                         video_name=image_paths[1],
                                                                         image_name=image_paths[2])

                    deal_path = os.path.join(deal_sample_disk, deal_image_formatten)
                    if not os.path.exists(source_path):
                        raise RuntimeError('source file not exist: %s' % (source_path,))

                    if not os.path.exists(deal_image_dir):
                        os.makedirs(deal_image_dir)
                    if is_had_deal(coon, image, int(PROCESS_TYPE.get(process_type))):
                        continue
                    try:
                        after_deal = processor.process(frame)
                    except MemoryError:
                        memoryerror_image_list.append(source_path)
                        print len(memoryerror_image_list)
                        continue

                    cv2.imwrite(deal_path, after_deal)
                    save_to_database(coon, image, deal_image_formatten, process_type)
            now_time = datetime.datetime.now()
            print 'last 1000 image process time : %s' % (now_time - last_start_time)
            print "id less than %s had process" % (last_id,)
            images = get_process_image(coon, last_id, business_type, target_process_type)
    except Exception, e:
        print e
        print traceback.format_exc()
    finally:
        coon.close()
        with open('memory_error.csv', 'wb') as m_f:
            writer = csv.writer(m_f)
            writer.writerows(memoryerror_image_list)






# def main2():
#     argparser = argparse.ArgumentParser('process all image resource')
#     argparser.add_argument('sample_dir', help='source image dir')
#     argparser.add_argument('deal_sample_disk', help='save image dir')
#     argparser.add_argument('process_types', nargs="+", help='blur10,blur20,blur30,blur40,blur50',
#                            choices=['blur10', 'blur20', 'blur30', 'blur40', 'blur50',
#                                     'mosaic5', 'mosaic10', 'mosaic15', 'mosaic20',
#                                     'colornoise50', 'colornoise100', 'colornoise150'])
#     args = argparser.parse_args()
#
#     sample_dir = args.sample_dir
#     deal_sample_disk = args.deal_sample_disk
#     process_types = args.process_types
#
#     deal_image_dir_format = 'deal_sample/{process_type}/{datetime}/{video_name}'
#     deal_image_path_format = 'deal_sample/{process_type}/{datetime}/{video_name}/{image_name}'
#
#     coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
#                            database.get('database'), charset='utf8')
#     # keys = ready_processors.keys()
#     keys = sorted(process_types)
#     image_queue = Queue.Queue()
#     try:
#         last_id = 0
#         image_queue = get_process_image(coon, last_id)
#         pros = mp.Pool(processes=2)
#
#         while image_queue.qsize() > 0:
#             # print 0
#             last_start_time = datetime.datetime.now()
#
#             results = []
#
#             while image_queue.qsize() > 0:
#
#                 iamge_item = image_queue.get()
#                 results.append(pros.apply_async(frame_process, args=(
#                         iamge_item, keys, sample_dir, deal_sample_disk, deal_image_dir_format, deal_image_path_format,)))
#                 last_id = iamge_item[0]
#             # pros.close()
#             # pros.join()
#             for i in results:
#                 i.get()  # 等待线程函数执行完毕
#
#             # for i in results:
#             #     if i.ready():  # 线程函数是否已经启动了
#             #         if i.successful():  # 线程函数是否执行成功
#             #             print(i.get())  # 线程函数返回值
#
#             now_time = datetime.datetime.now()
#             print 'last 1000 image process time : %s' % (now_time - last_start_time)
#             last_start_time = now_time
#             print "id less than %s had process" % (last_id,)
#             image_queue = get_process_image(coon, last_id)
#         pros.close()
#         pros.terminate()
#         pros.join()
#     except Exception, e:
#         msg = traceback.format_exc()
#         print msg
#     finally:
#         coon.close()

if __name__ == '__main__':
    # main()
    # update_processed_image()
    check_is_processed()

