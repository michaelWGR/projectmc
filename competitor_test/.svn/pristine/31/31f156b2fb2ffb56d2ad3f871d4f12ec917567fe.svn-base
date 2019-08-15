# /usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import producer
import numpy
import cv2
import os


def main():
    parser = argparse.ArgumentParser('\n\t组成数字的长条的宽（w）高（h）比为 k（暂时写死为 2）\n\
\t生成图片宽高计算公式如下：\n\t  W = (k+4)*h\n\t  H = (2k+5)*h\n')
    parser.add_argument('num', type=int)
    parser.add_argument('h', type=int, help='尽量使用偶数')
    parser.add_argument('--zfill', default=False,
                        type=int, help='数字总位数（不足前补0）')

    # parser.add_argument('--padding', default=20, type=int, help='数字和边框的间距')
    args = parser.parse_args()

    if args.zfill:
        num_fromat = '{:0>' + str(args.zfill) + 'd}'
        num_str = num_fromat.format(args.num)
    else:
        num_str = str(args.num)

    print 'num str to produce "{}"'.format(num_str)

    num_blocks = []
    pder = producer.Producer(args.h)
    for num in num_str:
        num_blocks.append(pder.produce(num))

    nums_block = None
    for num_block in num_blocks:
        if nums_block is None:
            nums_block = num_block
            continue
        nums_block = numpy.column_stack((nums_block, num_block))

    nums_block_shape = nums_block.shape
    # 暂定 20 像素
    padding = 20
    frame_block = numpy.zeros(
        (nums_block_shape[0] + padding * 2,
         nums_block_shape[1] + padding * 2, 3),
        dtype=numpy.uint8
    )
    frame_block.fill(255)

    numpy.copyto(frame_block[padding: padding + nums_block_shape[0],
                             padding: padding + nums_block_shape[1]], nums_block, casting='same_kind')

    # cv2.imshow('s', frame_block)
    # cv2.waitKey()

    output_dir = './masks'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    cv2.imwrite('{}/{}.bmp'.format(output_dir, num_str), frame_block)


if __name__ == '__main__':
    main()
