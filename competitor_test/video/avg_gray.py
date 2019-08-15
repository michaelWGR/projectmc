# -*- coding:utf-8 -*-

import argparse
import csv
import os

import cv2

from blackdetection import AverageGrayThresholdDetector

from utils import ROIFrameFilter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('--x', type=int)
    parser.add_argument('--y', type=int)
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('frame_path')
    args = parser.parse_args()

    frame_path = os.path.abspath(args.frame_path)

    x = args.x
    y = args.y
    width = args.width
    height = args.height

    frame_filter = None
    if x is not None and y is not None and width is not None and height is not None:
        frame_filter = ROIFrameFilter(x, y, width, height)

    frame = cv2.imread(frame_path)
    if frame_filter is not None:
        frame = frame_filter.filter(frame)

    black_detector = AverageGrayThresholdDetector(0)
    print black_detector.get_avg_gray(frame)


if __name__ == '__main__':
    main()