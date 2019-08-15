# -*- coding: utf-8 -*-

import argparse
import cv2
import numpy as np
import os

'''
    将 src_dir 作为遮罩层下的图片依次与 dst_dir 的图片合并生成新图片
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src_dir')
    parser.add_argument('dst_dir')
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src_dir)
    dst_dir = os.path.abspath(args.dst_dir)

    # 不要依赖 os.listdir() 返回 list 的顺序！！！！！
    # 临时使用，MAC 下文件名改为 000000.bmp~999999.bmp
    src_files = [os.path.join(src_dir, src_file) for src_file in os.listdir(
        src_dir) if src_file.endswith('.bmp')]

    dst_files = [os.path.join(dst_dir, dst_file) for dst_file in os.listdir(
        dst_dir) if dst_file.endswith('.bmp')]

    # print src_files[: 30]
    # print '---------------'
    # print dst_files[: 30]

    for i in range(0, 7806):
        # print src_files[i], dst_files[i]

        src = cv2.imread(src_files[i])
        cv2.namedWindow('src', cv2.WINDOW_NORMAL)
        # cv2.imshow('src', src)
        # cv2.waitKey(0)

        dst = cv2.imread(dst_files[i])
        cv2.namedWindow('dst', cv2.WINDOW_NORMAL)
        # cv2.imshow('dst', dst)
        # cv2.waitKey(0)

        #np.copyto(dst[360:360 + 354, 540: 540 + 866], src, casting='same_kind')
        np.copyto(dst[880: 880 + 130, 820: 820 + 280],
                  src, casting='same_kind')
        #cv2.imshow('dst', dst)
        # cv2.waitKey(0)
        # exit(0)

        output_dir = './hebing_quality'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        file_to_save = '%06d.bmp' % (i + 1)
        cv2.imwrite('%s/%s' % (output_dir, file_to_save), dst)
        print '%d frames saved.' % (i + 1)


if __name__ == '__main__':
    main()
