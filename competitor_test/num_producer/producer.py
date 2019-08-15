# /usr/bin/env python
# -*- coding:utf-8 -*-

import cv2
import numpy


class Producer(object):
    def __init__(self, h):
        # w:h == k
        self.k = 2
        self.h = h
        self.w = self.k * int(h)
        # 每个数字占块大小
        rect = ((2 * self.k + 5) * h, (self.k + 4) * h, 3)
        self.block = numpy.zeros(rect, dtype=numpy.uint8)
        # 初始化组成数字的横条和竖条
        self.row = numpy.zeros((h, self.w, 3), dtype=numpy.uint8)
        self.col = numpy.zeros((self.w, h, 3), dtype=numpy.uint8)
        # 填充数字条颜色为白色
        self.row.fill(255)
        self.col.fill(255)
        # 七个长条各自左上角坐标及长条类型（0 表示横条，1 表示竖条）
        # 暂定数字和框之间的 padding 为 h
        self.pos = {
            '1': (h, 2 * h, 0),
            '2': (2 * h, h, 1),
            '3': (2 * h, 2 * h + self.w, 1),
            '4': (2 * h + self.w, 2 * h, 0),
            '5': (3 * h + self.w, h, 1),
            '6': (3 * h + self.w, 2 * h + self.w, 1),
            '7': (3 * h + 2 * self.w, 2 * h, 0)
        }
        # 0～9 每个数字所对应七个长条的关系（0 表示不亮，1 表示亮）
        self.bitmap = {
            '0': (1, 1, 1, 0, 1, 1, 1),
            '1': (0, 0, 1, 0, 0, 1, 0),
            '2': (1, 0, 1, 1, 1, 0, 1),
            '3': (1, 0, 1, 1, 0, 1, 1),
            '4': (0, 1, 1, 1, 0, 1, 0),
            '5': (1, 1, 0, 1, 0, 1, 1),
            '6': (1, 1, 0, 1, 1, 1, 1),
            '7': (1, 0, 1, 0, 0, 1, 0),
            '8': (1, 1, 1, 1, 1, 1, 1),
            '9': (1, 1, 1, 1, 0, 1, 1)
        }

    def produce(self, num):
        if str(num) not in self.bitmap:
            print 'num must in 0~9'
            return None
        block = numpy.copy(self.block)
        for i, v in enumerate(self.bitmap.get(str(num))):
            # print i, v
            if v == 1:
                pos = self.pos.get(str(i + 1))
                if pos[2] == 1:
                    numpy.copyto(
                        block[pos[0]: pos[0] + self.w,
                              pos[1]: pos[1] + self.h],
                        self.col, casting='same_kind')
                else:
                    numpy.copyto(
                        block[pos[0]: pos[0] + self.h,
                              pos[1]: pos[1] + self.w],
                        self.row, casting='same_kind')

        return block

# test
# pd = Producer(80)
# img_num = pd.produce(9)

# cv2.namedWindow('img_num', cv2.WINDOW_NORMAL)
# cv2.imshow('img_num', img_num)
# cv2.waitKey()
