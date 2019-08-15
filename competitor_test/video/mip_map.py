# -*- coding:utf-8 -*-

import os
import sys
import cv2
import math
import numpy
import argparse

def mip_map_array(img, level):
    results = []

    results.append(img)
    cur_img = img
    for cur_level in range(0, level):
        cur_img = cv2.pyrDown(cur_img)
        results.append(cur_img)

    return results


def mip_map(img, level):
    width = img.shape[1]
    height = img.shape[0]
    channels = img.shape[2] if len(img.shape) > 2 else 1

    mip_map_width = width + width / 2 + width % 2
    mip_map_height = height
    mip_map_shape = (mip_map_height, mip_map_width, channels) if channels > 1 else (mip_map_height, mip_map_width)

    mip_map_img = numpy.zeros(mip_map_shape, img.dtype)
    numpy.copyto(mip_map_img[0:height,0:width], img)

    cur_img = img
    cur_x = width
    cur_y = 0
    for cur_level in range(0, level):
        cur_img = cv2.pyrDown(cur_img)
        cur_width = cur_img.shape[1]
        cur_height = cur_img.shape[0]
        numpy.copyto(mip_map_img[cur_y:cur_y+cur_height,cur_x:cur_x+cur_width], cur_img)
        cur_y = cur_y + cur_height

    return mip_map_img

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--width', type=int, help='width')
    # parser.add_argument('--height', type=int, help='height')
    parser.add_argument('--level', type=int, help='mip map level', default=3)
    parser.add_argument('--output-dir', help='output path')
    parser.add_argument('input_dir')
    args = parser.parse_args()

    level = args.level

    valid_exts = [ '.bmp' ]
    input_dir = os.path.abspath(args.input_dir)
    # output_dir = os.path.abspath(args.output_dir) if args.output_dir is not None else input_dir

    if args.output_dir is None:
        output_dir = os.path.join(input_dir, 'mip_map')
    else:
        output_dir = args.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frame_paths = [ os.path.join(input_dir, _) for _ in os.listdir(input_dir) if os.path.splitext(_)[1] in valid_exts ]
    
    for cur_level in range(1, level + 1):
        level_dir = os.path.join(output_dir, str(cur_level))
        if not os.path.exists(level_dir):
            os.makedirs(level_dir)

    for frame_path in frame_paths:
        print 'input',frame_path
        frame_name = os.path.basename(frame_path)
        frame_img = cv2.imread(frame_path)
        mip_map_imgs = mip_map_array(frame_img, level)
        for cur_level in range(1, level + 1):
            mip_map_path = os.path.join(output_dir, str(cur_level), frame_name)
            print 'output',mip_map_path
            cv2.imwrite(mip_map_path, mip_map_imgs[cur_level])

        # mip_map_img = mip_map(frame_img, level)
        # mip_map_path = os.path.join(output_dir, frame_name)
        # print 'output',mip_map_path
        # cv2.imwrite(mip_map_path, mip_map_img)
