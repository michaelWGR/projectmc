# -*- coding:utf-8 -*-

import argparse
import csv
import os

import cv2

from blackdetection import AverageGrayThresholdDetector
from blackframe import BlackFrameDetector
from utils import get_video_shape, VideoFrameGenerator


def get_frame_generator(video_path, frame_rate):
    video_shape = get_video_shape(video_path)
    return VideoFrameGenerator(video_path, video_shape, frame_rate)


def get_black_results_file(video_path):
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(video_dir, '%s.csv' % (video_name, ))


def parse_black_results(black_results, frame_rate):
    parse_results = []

    prev_black_result = None
    blacking = None
    old_blacking = None
    for black_result in black_results:
        if blacking is None:
            blacking = black_result.result.is_black
        else:
            old_blacking = blacking
            blacking = black_result.result.is_black

            if old_blacking != blacking:
                parse_results.append([None, None, black_result.frame_num, frame_rate, float(black_result.frame_num) / frame_rate, black_result.result.avg_gray])

        prev_black_result = black_result
    return parse_results


def write_black_results(black_results_file, frame_rate, black_results):
    with open(black_results_file, 'wb') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['frame', 'frame_rate', 'time', 'avg_gray'])
        for black_result in black_results:
            csv_writer.writerow([black_result.frame_num, frame_rate, float(black_result.frame_num) / frame_rate, black_result.result.avg_gray])


def resize_frame(frame, width=400):
    return cv2.resize(frame, (width, int(round(float(width) / frame.shape[1] * frame.shape[0]))))


def main():
    import cv2
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-sr', '--src-frame-rate', type=float, default=60, help='source frame rate')
    parser.add_argument('-tr', '--target-frame-rate', type=float, default=None, help='target frame rate')
    parser.add_argument('-t', '--black-threshold', type=int, default=30, help='black threshold') # other < 20 but xm < 30
    parser.add_argument('-st', '--src-black-threshold', type=int, help='black threshold') # other < 20 but xm < 30
    parser.add_argument('-tt', '--target-black-threshold', type=int, help='black threshold') # other < 20 but xm < 30
    parser.add_argument('src_video_path')
    parser.add_argument('target_video_path')
    parser.add_argument('output_file')
    args = parser.parse_args()

    verbose = args.verbose

    src_video_path = os.path.abspath(args.src_video_path)
    src_black_results_file = get_black_results_file(src_video_path) if verbose else None

    src_frame_rate = args.src_frame_rate

    target_video_path = os.path.abspath(args.target_video_path)
    target_black_results_file = get_black_results_file(target_video_path) if verbose else None

    target_frame_rate = args.target_frame_rate if args.target_frame_rate is not None else src_frame_rate

    # black_threshold = args.black_threshold
    src_black_threshold = args.src_black_threshold if args.src_black_threshold is not None else args.black_threshold
    target_black_threshold = args.target_black_threshold if args.target_black_threshold is not None else args.black_threshold

    output_file = args.output_file

    src_black_detector = AverageGrayThresholdDetector(src_black_threshold)
    target_black_detector = AverageGrayThresholdDetector(target_black_threshold)

    src_black_results = BlackFrameDetector(get_frame_generator(src_video_path, src_frame_rate), src_black_detector).detect()
    target_black_results = BlackFrameDetector(get_frame_generator(target_video_path, target_frame_rate), target_black_detector).detect()

    src_parse_results = parse_black_results(src_black_results, src_frame_rate)
    target_parse_results = parse_black_results(target_black_results, target_frame_rate)

    if src_black_results_file is not None:
        write_black_results(src_black_results_file, src_frame_rate, src_black_results)
    if target_black_results_file is not None:
        write_black_results(target_black_results_file, target_frame_rate, target_black_results)

    black_frame_count = max(len(src_parse_results), len(target_parse_results))

    with open(output_file, 'wb') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['src_frame', 'src_frame_rate','src_time','src_avg_gray','target_frame', 'target_frame_rate','target_time','target_avg_gray','diff_time'])
        for i in range(0, black_frame_count):
            if len(src_parse_results) > 0:
                src_parse_result = src_parse_results[i] if i < len(src_parse_results) else src_parse_results[len(src_parse_results) - 1]
            else:
                src_parse_result = [None, None, 0, src_frame_rate, 0, 0]

            if len(target_parse_results) > 0:
                target_parse_result = target_parse_results[i] if i < len(target_parse_results) else target_parse_results[len(target_parse_results) - 1]
            else:
                target_parse_result = [None, None, 0, target_frame_rate, 0, 0]

            row = src_parse_result[2:] + target_parse_result[2:] + [abs(src_parse_result[4] - target_parse_result[4])]

            csv_writer.writerow(row)


if __name__ == '__main__':
    main()