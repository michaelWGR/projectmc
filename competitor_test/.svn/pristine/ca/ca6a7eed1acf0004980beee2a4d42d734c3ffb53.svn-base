# /usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import os
import cv2

from cut_config import CONFIG

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


def process(args):
    origin_dir = os.path.normpath(args.origin_dir)

    suffix = '_' + args.roi_type + '_roi' if args.roi_type else '_roi'
    target_dir = origin_dir + suffix
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    print('%s processing...' % origin_dir)

    if args.roi_type:
        pre_roi_param = CONFIG[args.roi_type].get('pre_roi')
        resize_param = CONFIG[args.roi_type].get('resize')
        roi_param = CONFIG[args.roi_type].get('roi')
        print('roi_type assigned. Use %s roi param in config:\n  \
pre_roi_param: %s\n  resize_param: %s\n  roi_param: %s' %
              (args.roi_type, pre_roi_param, resize_param, roi_param))
    else:
        pre_roi_param = {
            'x': args.pre_x, 'y': args.pre_y,
            'width': args.pre_width, 'height': args.pre_height
        }
        resize_param = {
            'width': args.resize_width, 'height': args.resize_height
        }
        roi_param = {
            'x': args.x, 'y': args.y,
            'width': args.width, 'height': args.height
        }

    count = 0  # 进度计数器，达到1000张图片输出一次 log
    for file in os.listdir(origin_dir):
        if file.endswith('.bmp') or file.endswith('.BMP'):
            path = os.path.join(origin_dir, file)
            image = cv2.imread(path)
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

            cv2.imwrite(os.path.join(target_dir, file), image)

            # 进度计数器，与图片处理逻辑无关，可忽略
            if (count + 1) / 1000 > count / 1000:
                print('%d pics finished' % (count + 1))
            count += 1


def main():
    parser = argparse.ArgumentParser()

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

    parser.add_argument('origin_dir')
    args = parser.parse_args()

    process(args)


if __name__ == '__main__':
    main()
