# -*- coding:utf-8 -*-

import argparse
import csv
import os

from blackdetection import AverageGrayThresholdDetector
from blackframe import BlackFrameDetector
from utils import ROIFrameFilter, get_video_shape, VideoFrameGenerator


def get_frame_generator(video_path, frame_rate):
    video_shape = get_video_shape(video_path)
    return VideoFrameGenerator(video_path, video_shape, frame_rate)


def get_avggray_file(video_path):
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(video_dir, '%s_avggray.csv' % (video_name, ))


def get_parse_results_file(video_path):
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(video_dir, '%s.csv' % (video_name, ))


def parse_black_results(black_results, frame_rate):
    parse_results = []

    blacking = None
    old_blacking = None
    for black_result in black_results:
        if blacking is None:
            blacking = black_result.result.is_black
        else:
            old_blacking = blacking
            blacking = black_result.result.is_black

            if old_blacking != blacking:
                parse_results.append([black_result.frame_num, frame_rate, float(black_result.frame_num) / frame_rate, black_result.result.avg_gray])
    return parse_results


def write_black_results(black_results_file, frame_rate, black_results):
    with open(black_results_file, 'wb') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['frame', 'frame_rate', 'time', 'avg_gray'])
        for black_result in black_results:
            csv_writer.writerow([black_result.frame_num, frame_rate, float(black_result.frame_num) / frame_rate, black_result.result.avg_gray])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', type=float, default=60, help='frame rate')
    parser.add_argument('-t', '--black-threshold', type=int, default=14, help='black threshold') # audio delay = 14
    parser.add_argument('--x', type=int)
    parser.add_argument('--y', type=int)
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('-vf', '--avggray-file', action='store_true', default=False, help='avggray file')
    parser.add_argument('--output-file', help='output file')
    parser.add_argument('video_paths', nargs='+')
    args = parser.parse_args()

    verbose = args.verbose
    frame_rate = args.frame_rate

    black_threshold = args.black_threshold

    output_avggray_file = args.avggray_file

    for video_path in args.video_paths:
        video_path = os.path.abspath(video_path)
        output_file = args.output_file if args.output_file is not None else get_parse_results_file(video_path)

        x = args.x
        y = args.y
        width = args.width
        height = args.height

        frame_filter = None
        if x is not None and y is not None and width is not None and height is not None:
            frame_filter = ROIFrameFilter(x, y, width, height)

        black_detector = AverageGrayThresholdDetector(black_threshold)
        black_results = BlackFrameDetector(get_frame_generator(video_path, frame_rate), black_detector, frame_filter=frame_filter).detect()

        if output_avggray_file:
            avggray_file = get_avggray_file(video_path)
            write_black_results(avggray_file, frame_rate, black_results)

        parse_results = parse_black_results(black_results, frame_rate)

        with open(output_file, 'wb') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['frame', 'frame_rate','time','avg_gray'])
            for parse_result in parse_results:
                csv_writer.writerow(parse_result)

if __name__ == '__main__':
    main()