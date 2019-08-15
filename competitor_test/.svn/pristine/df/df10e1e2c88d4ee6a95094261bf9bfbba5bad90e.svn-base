# -*- coding:utf-8 -*-

import argparse
import os

import cv2
import numpy

from utils import get_video_shape, VideoFrameGenerator
from cut_config import CONFIG

__author__ = 'LibX'

def extract_frame(args, video_path):
    video_path = os.path.abspath(video_path)
    video_file = os.path.basename(video_path)
    video_name = os.path.splitext(video_file)[0]  
    frame_rate = args.frame_rate if args.frame_rate is not None else None   
    frame_nums = args.frame_nums if args.frame_nums is not None and len(args.frame_nums) > 0 else None
    distinct = args.distinct if args.distinct is not None else False
    video_shape = get_video_shape(video_path)

    if frame_nums is None:
     
        frame_generator = VideoFrameGenerator(video_path, video_shape, frame_rate)

        with frame_generator as frames:
            i = 1
            prev_frame = None
            for frame in frames:
                should_write = True
                if prev_frame is not None and args.distinct:
                    should_write = not numpy.array_equal(prev_frame, frame)
                    
                if should_write:
                    process(args, video_path, frame, i)
                prev_frame = frame
                i += 1

    else:
        frame_nums = sorted(frame_nums)
        max_frame_num = max(frame_nums)
        frame_generator = VideoFrameGenerator(video_path, video_shape, frame_rate)

        with frame_generator as frames:
            frame_num_index = 0
            frame_num = frame_nums[frame_num_index]
            i = 1

            for frame in frames:
                should_write = False
                if frame_nums is None:
                    # no frame_nums, write all
                    should_write = True
                else:
                    if i > max_frame_num:
                        break

                    if i == frame_num:
                        should_write = True
                        frame_num_index += 1
                        if frame_num_index < len(frame_nums):
                            frame_num = frame_nums[frame_num_index]

                if should_write:
                    process(args, frame, i)
                i += 1


def resize(image, width, height):
    # print resize_width, resize_height
    width = width if width else image.shape[1]
    height = height if height else image.shape[0]

    res = cv2.resize(image, (width, height), interpolation=cv2.INTER_LANCZOS4)
    return res


def roi(image, x, y, width, height):
    # print x, y, width, height
    x = x if x else 0
    y = y if y else 0
    width = width if width else (image.shape[1] - x)
    height = height if height else (image.shape[0] - y)

    res = image[y:y + height, x:x + width]
    return res


def process(args, video_path, image, count):
    #import ipdb;ipdb.set_trace()
    origin_dir, video_file = os.path.split(video_path)
    #video_file = os.path.basename(origin_dir)
    video_name = os.path.splitext(video_file)[0]
    suffix = video_name+'_'+args.roi_type + '_roi' if args.roi_type else '_roi'
    target_dir = os.path.join(origin_dir, suffix)
    frame_type = args.frame_type if args.frame_type is not None else 'jpg'
    frames_file_pattern = os.path.join(target_dir, video_name + '%05d.' + frame_type)

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)


    if args.roi_type:
        pre_roi_param = CONFIG[args.roi_type].get('pre_roi')
        resize_param = CONFIG[args.roi_type].get('resize')
        roi_param = CONFIG[args.roi_type].get('roi')

    else:
        pre_roi_param = {
            'x': args.pre_x, 'y': args.pre_y,
            'pre_width': args.pre_width, 'pre_height': args.pre_height
        }
        resize_param = {
            'width': args.resize_width, 'height': args.resize_height
        }
        roi_param = {
            'x': args.x, 'y': args.y,
            'width': args.width, 'height': args.height
        }

    # 去黑边（前切图）
    if not args.no_pre_roi and pre_roi_param:
        image = roi(image,
                    pre_roi_param['x'], pre_roi_param['y'],
                    pre_roi_param['width'], pre_roi_param['height'])
    # 放大
    if not args.no_resize and resize_param:
        image = resize(
            image, resize_param['width'], resize_param['height'])
    # 后切图
    if not args.no_after_roi and roi_param:
        image = roi(image,
                    roi_param['x'], roi_param['y'],
                    roi_param['width'], roi_param['height'])

    cv2.imwrite(frames_file_pattern % (count,), image)
    if (count + 1) / 1000 > count / 1000:
        print('%d pics finished' % (count + 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', type=float, help='frame rate')
    parser.add_argument('-d', '--distinct',type=bool, help='distinct')
    parser.add_argument('-n', '--frame-nums', nargs='*', type=int, help='frame nums')
    parser.add_argument('-t', '--frame-type', help='frame type')
    #parser.add_argument('--output-dir', help='output dir')
    parser.add_argument('--pre-x', type=int)
    parser.add_argument('--pre-y', type=int)
    parser.add_argument('--pre-width', type=int)
    parser.add_argument('--pre-height', type=int)

    parser.add_argument('--resize-width', type=int)
    parser.add_argument('--resize-height', type=int)

    parser.add_argument('--x', type=int)
    parser.add_argument('--y', type=int)
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)

    parser.add_argument('--roi-type', choices=CONFIG.keys(),
                        help='If this param assigned, \
                        use size params in CONFIG.')

    parser.add_argument('--no-resize', action='store_true', default=False)
    parser.add_argument('--no-pre-roi', action='store_true', default=False)
    parser.add_argument('--no-after-roi', action='store_true', default=False)

    parser.add_argument('video_paths', nargs='+')
    args = parser.parse_args()

    for video_path in args.video_paths:
        extract_frame(args, video_path)

 

if __name__ == "__main__":
    main()
