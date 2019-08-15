# -*- coding:utf-8 -*-

import argparse
import os

import cv2

from utils import get_video_shape, VideoFrameGenerator

__author__ = 'LibX'


def view_frame(video_path, video_shape, frame_rate, frame_nums):
    frame_nums = sorted(frame_nums)
    max_frame_num = max(frame_nums)

    frame_generator = VideoFrameGenerator(video_path, video_shape, frame_rate)
    with frame_generator as frames:
        tmp_frames = []
        frame_num_index = 0
        frame_num = frame_nums[frame_num_index]
        i = 1
        for frame in frames:
            if i > max_frame_num + 1:
                break

            if frame_num - 1 <= i <= frame_num + 1:
                tmp_frames.append(frame)

            if i == frame_num + 1:
                for j in [_ for _ in range(0, 3) if frame_num - 1 + _ > 0]:
                    cv2.imshow('frame %d' % (frame_num - 1 + j), tmp_frames[j])
                cv2.waitKey(0)

                cv2.destroyAllWindows()

                tmp_frames = []
                frame_num_index += 1
                if frame_num_index < len(frame_nums):
                    frame_num = frame_nums[frame_num_index]

            i += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('video_path', help='video path')
    parser.add_argument('frame_rate', type=float, help='frame rate')
    parser.add_argument('frame_nums', nargs='+', type=int, help='frame nums')
    args = parser.parse_args()

    video_path = os.path.abspath(args.video_path)
    frame_rate = args.frame_rate
    frame_nums = args.frame_nums

    video_shape = get_video_shape(video_path)
    view_frame(video_path, video_shape, frame_rate, frame_nums)


if __name__ == "__main__":
    main()