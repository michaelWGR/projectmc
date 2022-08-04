# -*- coding:utf-8 -*-
# from __future__ import absolute_import
import argparse
import sys
import cv2
import numpy
import datetime
import threading
import queue
import os

# import MySQLdb
import traceback

from utils.settings import *
from utils import get_video_shape, VideoFrameGenerator

import django
from django.db import transaction
sys.path.append(PROJ_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'aiResource.settings'
django.setup()

from management.models import Resource


deal_ext = ('.mp4', '.flv', '.avi', '.mov')


class VideoMeta(object):
    def __init__(self, video_path, output_disk):
        self.video_path = os.path.abspath(video_path)
        self.video_dir = os.path.dirname(self.video_path)
        self.video_name = os.path.basename(self.video_path)
        self.video_name_noext = self.video_name.split('.')[0]
        self.abs_output_dir = os.path.abspath(output_disk)

        self.frames_file_path = 'sample/{datetime}/{video_name}/{video_name}_%06d.jpg'.format(
            datetime=datetime.datetime.now().strftime('%Y%m%d'), video_name=self.video_name_noext)
        self.frames_file_pattern = os.path.join(self.abs_output_dir, self.frames_file_path)

        self.frames_file_dir = os.path.dirname(self.frames_file_pattern)
        self.frames_file_url = 'http://ai-resource.yypm.com/resource/' + self.frames_file_path
        self.meta_path = os.path.join(self.video_dir, "." + self.video_name_noext + '.meta', )


def extract_frame(video_meta, video_shape, frames_file_pattern, frame_rate=None, distinct=False):
    frames_dirs = []
    frames_dirs.append(video_meta.video_path + os.linesep)

    frame_generator = VideoFrameGenerator(video_meta.video_path, video_shape, frame_rate)
    with frame_generator as frames:
        i = 1
        prev_frame = None
        for frame in frames:
            should_write = True
            if prev_frame is not None and distinct:
                should_write = not numpy.array_equal(prev_frame, frame)

            if should_write:
                frame_path = frames_file_pattern % (i,)
                cv2.imwrite(frame_path, frame)
                # write to meta
                frames_dirs.append(video_meta.frames_file_url % (i,) + os.linesep)

            prev_frame = frame
            i += 1
    return frames_dirs


def save_to_database(meta_file_path, business_type, col_int_01):
    # persist to database
    # prepare video
    # meta_file_paths = []
    # for root, dirs, files in os.walk(video_dir):
    #     if files:
    #         for file_ in files:
    #             if file_.endswith('.meta'):
    #                 meta_file_paths.append(os.path.join(root, file_))

    # coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
    #                        database.get('database'), charset='utf8')

    check_is_insert = 'select count(*) from resources where path = %s'
    insert_sql = "insert into resources(path,type,process_type,pid,pre_id,next_id, is_leaf,ctime,mtime) values(%s,%s,%s,%s,%s,0,%s,%s,%s)"
    update_next_id_sql = 'update resources set next_id=%s, mtime=%s WHERE id=%s'
    update_last_line_sql = 'update resources set next_id=0, is_leaf=1, mtime = %s WHERE id= %s'

    # for meta_file_path in meta_file_paths:

    # cursor = coon.cursor()
    # transaction.set_autocommit(False)

    with open(meta_file_path, 'rb') as meta_file:
        is_video_line = True
        is_first_frame_line = True
        video_id = 0
        pre_id = None
        try:
            for line in meta_file:
                line = line.strip()
                # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if is_video_line:
                    # cursor.execute(check_is_insert, (line,))
                    # results = cursor.fetchall()
                    # if int(results[0][0]) >= 1:
                    #     print 'video %s have insert' % (line,)
                    #     break
                    #
                    # cursor.execute(insert_sql, (line, 0, 0, 0, 0, 0, now_time, now_time))
                    # video_id = coon.insert_id()
                    is_had = Resource.objects.filter(path=line).count()
                    if is_had >= 1:
                        print('video %s have insert' % (line,))
                        break
                    resource = Resource(path=line, type=0, business_type=business_type, pid=0, pre_id=0,
                                        next_id=0, checked=0, process_type=0, is_leaf=1, is_debug=0,
                                        col_int_01=col_int_01)
                    resource.save()
                    video_id = resource.id
                    is_video_line = False

                else:

                    if is_first_frame_line:
                        # cursor.execute(insert_sql, (line, 1, 0, video_id, 0, 0, now_time, now_time,))
                        # pre_id = coon.insert_id()
                        resource = Resource(path=line, type=1, business_type=business_type, pid=video_id, pre_id=0,
                                            next_id=0, checked=0, process_type=1, is_leaf=1, is_debug=0,
                                            col_int_01=col_int_01)
                        resource.save()
                        pre_id = resource.id
                        is_first_frame_line = False
                    else:
                        # print pre_id
                        # cursor.execute(insert_sql, (line, 1, 0, video_id, pre_id, 0, now_time, now_time,))
                        # new_line_id = coon.insert_id()
                        # # print new_line_id
                        # cursor.execute(update_next_id_sql, (new_line_id, now_time, pre_id))
                        # pre_id = new_line_id

                        # cursor.execute(update_last_line_sql, (now_time, pre_id))

                        resource = Resource(path=line, type=1, business_type=business_type, pid=video_id,
                                            pre_id=pre_id, next_id=0, checked=0, process_type=1, is_leaf=1, is_debug=0,
                                            col_int_01=col_int_01)
                        resource.save()
                        new_line_id = resource.id

                        # cursor.execute(update_next_id_sql, (new_line_id, now_time, pre_id))
                        Resource.objects.filter(id=pre_id).update(next_id=new_line_id)
                        pre_id = new_line_id
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise RuntimeError(e)


class DealThread(threading.Thread):
    def __init__(self, video_metas, frame_rate, distinct, business_type, col_int_01):
        threading.Thread.__init__(self)
        self.video_metas = video_metas
        self.frame_rate = frame_rate
        self.distinct = distinct
        self.business_type = business_type
        self.col_int_01 = col_int_01

    def run(self):
        while not self.video_metas.empty():
            video_meta = None
            try:
                print('undeal %d' % (self.video_metas.qsize(),))
                video_meta = self.video_metas.get()
                if not os.path.exists(video_meta.frames_file_dir):
                    os.makedirs(video_meta.frames_file_dir)

                if os.path.exists(video_meta.meta_path) and os.path.isfile(video_meta.meta_path):
                    print ('video %s had deal' % (video_meta.video_path,))
                    # selvideo_metas.remove(video_meta)
                    continue

                video_shape = get_video_shape(video_meta.video_path)
                frames_dirs = self.extract_frame(video_meta, video_shape, video_meta.frames_file_pattern,
                                                 frame_rate=self.frame_rate,
                                                 distinct=self.distinct)
                with open(video_meta.meta_path, 'wb') as meta_file:
                    meta_file.writelines(frames_dirs)

                self.save_to_database(video_meta.meta_path)
            except Exception as e:
                print('threading error')
                print(os.path.exists(video_meta.meta_path))
                if os.path.exists(video_meta.meta_path):

                    os.remove(video_meta.meta_path)
                raise RuntimeError()


    @staticmethod
    def extract_frame(video_meta, video_shape, frames_file_pattern, frame_rate=None, distinct=False):
        print('threading extrat')
        frames_dirs = []
        frames_dirs.append(video_meta.video_path + os.linesep)

        frame_generator = VideoFrameGenerator(video_meta.video_path, video_shape, frame_rate)
        with frame_generator as frames:
            i = 1
            prev_frame = None
            for frame in frames:
                should_write = True
                if prev_frame is not None and distinct:
                    should_write = not numpy.array_equal(prev_frame, frame)

                if should_write:
                    frame_path = frames_file_pattern % (i,)
                    cv2.imwrite(frame_path, frame)
                    # write to meta
                    frames_dirs.append(video_meta.frames_file_url % (i,) + os.linesep)

                prev_frame = frame
                i += 1
        # frames_dirs.append('end' + os.linesep)
        return frames_dirs

    # @staticmethod
    def save_to_database(self, meta_file_path):
        print('threading save')
        # persist to database
        # prepare video
        # meta_file_paths = []
        # for root, dirs, files in os.walk(video_dir):
        #     if files:
        #         for file_ in files:
        #             if file_.endswith('.meta'):
        #                 meta_file_paths.append(os.path.join(root, file_))
        is_debug = 0

        # coon = MySQLdb.connect(database.get('host'), database.get('user'), database.get('password'),
        #                        database.get('database'), charset='utf8')

        check_is_insert = 'select count(*) from resources where path = %s'
        insert_sql = "insert into resources(path,type,business_type,pid,pre_id,next_id, checked, process_type,is_leaf,is_debug, col_int_01,ctime,mtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        update_next_id_sql = 'update resources set next_id=%s, mtime=%s WHERE id=%s'
        update_last_line_sql = 'update resources set next_id=0, mtime=%s WHERE id=%s'

        # for meta_file_path in meta_file_paths:

        # cursor = coon.cursor()
        transaction.set_autocommit(False)
        count = 0
        try:
            with open(meta_file_path, 'rb') as meta_file:
                is_video_line = True
                is_first_frame_line = True
                video_id = 0
                pre_id = 0
                for line in meta_file:
                    # print count
                    # count = count + 1
                    # if count > 3:
                    #     raise RuntimeError('999999')
                    line = line.strip()
                    # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if is_video_line:
                        is_had = Resource.objects.filter(path=line).count()
                        if is_had >= 1:
                            print('video %s have insert' % (line,))
                            break
                        resource = Resource(path=line, type=0, business_type=self.business_type, pid=0, pre_id=0,
                                            next_id=0, checked=0, process_type=0, is_leaf=1, is_debug=0,
                                            col_int_01=self.col_int_01)
                        resource.save()
                        video_id = resource.id

                        # cursor.execute(insert_sql, (line, 0, self.business_type, 0, 0, 0, 0, 0, 0, is_debug, self.col_int_01, now_time, now_time))
                        # video_id = coon.insert_id()
                        is_video_line = False
                    else:
                        if is_first_frame_line:
                            # cursor.execute(insert_sql,
                            #                (line, 1, self.business_type, video_id, 0, 0, 0, 1, 1, is_debug, self.col_int_01, now_time, now_time,))
                            # pre_id = coon.insert_id()
                            resource = Resource(path=line, type=1, business_type=self.business_type, pid=video_id, pre_id=0,
                                                next_id=0, checked=0, process_type=1, is_leaf=1, is_debug=0,
                                                col_int_01=self.col_int_01)
                            resource.save()
                            pre_id = resource.id
                            is_first_frame_line = False
                        elif line:
                            # cursor.execute(insert_sql, (
                            # line, 1, self.business_type, video_id, pre_id, 0, 0, 1, 1, is_debug, self.col_int_01, now_time, now_time,))
                            # new_line_id = coon.insert_id()
                            resource = Resource(path=line, type=1, business_type=self.business_type, pid=video_id,
                                                pre_id=pre_id,
                                                next_id=0, checked=0, process_type=1, is_leaf=1, is_debug=0,
                                                col_int_01=self.col_int_01)
                            resource.save()
                            new_line_id = resource.id

                            # cursor.execute(update_next_id_sql, (new_line_id, now_time, pre_id))
                            Resource.objects.filter(id=pre_id).update(next_id=new_line_id)
                            pre_id = new_line_id
                            # cursor.execute(update_last_line_sql, (now_time, pre_id))
                            # Resource.objects.filter(id=pre_id)
                transaction.commit()
        except Exception as e:
            print(traceback.format_exc())
            # cursor.close()
            transaction.rollback()
            raise RuntimeError(e)
            # coon.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', type=float, help='frame rate', default='1.0')
    parser.add_argument('-d', '--distinct', action='store_true', default=False, help='distinct')
    parser.add_argument('-t', '--frame-type', help='frame type')
    parser.add_argument('video_dir', help='video\'s dir')
    parser.add_argument('output_disk', help='output disk')
    parser.add_argument('business_type', help="pron:0, ad_orc:1, game_ocr:2", choices=['0', '1', '2'])
    parser.add_argument('col_int_01', help='game type or something else',
                        choices=['juediqiusheng', 'huangyexingdong', 'cijizhanchang', 'quanjunchuji', 'wangzherongyao'])
    args = parser.parse_args()

    frame_rate = args.frame_rate
    distinct = args.distinct
    frame_type = args.frame_type if args.frame_type is not None else 'jpg'
    output_disk = args.output_disk
    business_type = args.business_type
    col_int_01 = args.col_int_01

    if not os.path.exists(args.video_dir):
        raise RuntimeError('video dir ' + args.video_dir + 'not exists')

    if not os.path.exists(output_disk):
        raise RuntimeError('output disk ' + args.output_disk + 'not exists')

    # prepare video
    video_metas = []
    video_metas_queue = queue.Queue()
    for root, dirs, files in os.walk(args.video_dir):
        if files:
            for file_ in files:
                # print file_
                if file_.lower().endswith(deal_ext):
                    video_metas_queue.put(VideoMeta(os.path.join(root, file_), output_disk))


    video_meta = None
    try:
        while video_metas_queue.qsize() > 0:
            video_meta = video_metas_queue.get()
            print("undeal video %s" % (video_metas_queue.qsize()))
            if not os.path.exists(video_meta.frames_file_dir):
                os.makedirs(video_meta.frames_file_dir)

            if os.path.exists(video_meta.meta_path) and os.path.isfile(video_meta.meta_path):
                print('video %s had deal' % (video_meta.video_path,))
                continue

            video_shape = get_video_shape(video_meta.video_path)
            frames_dirs = extract_frame(video_meta, video_shape, video_meta.frames_file_pattern, frame_rate=frame_rate,
                                        distinct=distinct)
            with open(video_meta.meta_path, 'w') as meta_file:
                meta_file.writelines(frames_dirs)

            save_to_database(video_meta.meta_path, business_type, GameType[col_int_01].value)
    except Exception:
        if os.path.exists(video_meta.meta_path):
            os.remove(video_meta.meta_path)

        print(traceback.format_exc())


    # threads = []
    # try:
    #     for i in range(0, 1):
    #         tmp_thread = DealThread(video_metas_queue, frame_rate, distinct, business_type=business_type,
    #                                 col_int_01=GameType[col_int_01].value)
    #         tmp_thread.start()
    #         threads.append(tmp_thread)
    #     for thread in threads:
    #         thread.join()
    # except Exception, e:
    #     print traceback.format_exc()


if __name__ == "__main__":
    main()
