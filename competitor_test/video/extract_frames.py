# -*- coding:utf-8 -*-

import argparse
import os

import cv2
import numpy

from utils import get_video_shape, VideoFrameGenerator

__author__ = 'LibX'


def extract_frame(video_path, video_shape, frames_dir, frame_rate=None, distinct=False, frame_nums=None, frame_type='jpg'):
    video_file = os.path.basename(video_path)
    video_name = os.path.splitext(video_file)[0]
    frames_file_pattern = os.path.join(frames_dir, video_name + '%05d.' + frame_type)
    
    if frame_nums is None:
        frame_generator = VideoFrameGenerator(video_path, video_shape, frame_rate)
        with frame_generator as frames:
            i = 1
            prev_frame = None
            for frame in frames:
                should_write = True
                if prev_frame is not None and distinct:
                    should_write = not numpy.array_equal(prev_frame, frame)
                    
                if should_write:
                    cv2.imwrite(frames_file_pattern % (i,), frame)
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
                    cv2.imwrite(frames_file_pattern % (i,), frame)

                i += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', type=float, help='frame rate')
    parser.add_argument('-d', '--distinct', action='store_true', default=False, help='distinct')
    parser.add_argument('-n', '--frame-nums', nargs='*', type=int, help='frame nums')
    parser.add_argument('-t', '--frame-type', help='frame type')
    parser.add_argument('--output-dir', help='output dir')
    parser.add_argument('video_paths', nargs='+')
    args = parser.parse_args()

    frame_rate = args.frame_rate
    distinct = args.distinct
    frame_nums = args.frame_nums if args.frame_nums is not None and len(args.frame_nums) > 0 else None
    frame_type = args.frame_type if args.frame_type is not None else 'jpg'

    for video_path in args.video_paths:
        video_path = os.path.abspath(video_path)
        video_file = os.path.basename(video_path)
        video_name = os.path.splitext(video_file)[0]

        frames_dir = args.output_dir
        if frames_dir is None:
            frames_basedir = os.path.dirname(video_path)
            frames_dir = os.path.join(frames_basedir, video_name)

            if not os.path.exists(frames_dir):
                os.mkdir(frames_dir)

        video_shape = get_video_shape(video_path)
        extract_frame(video_path, video_shape, frames_dir, frame_rate=frame_rate, distinct=distinct, frame_nums=frame_nums, frame_type=frame_type)


if __name__ == "__main__":
    main()
