# -*- coding:utf-8 -*-
from __future__ import print_function
import argparse

import logging.config
import os
import cv2

# log config
logging_config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s.%(funcName)s] %(message)s'
        }
    },
    'handlers': {
        # 'file': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'filename': os.path.join(settings.BASE_DIR, 'log/combine_images.log'),
        #     'when': 'midnight',
        #     'formatter': 'standard',
        # },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        'combine_images': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger('combine_images')


class Images:
    def __init__(self, images_format):
        self.images_format = images_format

    def iter(self, num=1):
        """
        图片迭代器
        :param num: 默认为1，后续如果需要扩展再替换参数即可
        :return:
        """
        i = num
        while True:
            try:
                img_file = self.images_format % i
                if os.path.isfile(img_file):
                    yield img_file
                    i += 1
                else:
                    raise StopIteration('{} is not found, please check your file format {}'.format(img_file,
                                                                                                   self.images_format))
            except TypeError as e:
                logger.exception('parse images format error, please check your format: {} ', self.images_format, e)


def combine_images(img_base, img_over, img_name):
    """
    合成图片
    :param img_base: 底片
    :param img_over: 嵌在底片中间的图片
    :param img_name: 生成的图片名字
    :return:
    """
    logger.debug('Combining img_base {} and img_over {} to {}'.format(img_base, img_over, img_name))
    base = cv2.imread(img_base)
    over = cv2.imread(img_over)

    base_y, base_x = base.shape[0], base.shape[1]
    over_y, over_x = over.shape[0], over.shape[1]

    # check resolution
    if base_y < over_y or base_x < base_y:
        raise ValueError('base_y is smaller than over_y or base_x is smaller than base_y')

    # get center offset
    offset_y = base_y / 2 - over_y / 2
    offset_x = base_x / 2 - over_x / 2

    base[offset_y:offset_y + over_y, offset_x:offset_x + over_x] = over
    cv2.imwrite(img_name, base)


def main():
    parser = argparse.ArgumentParser(description='合并图片')
    parser.add_argument('base_images', help='base images.')
    parser.add_argument('over_images', help='over images.')
    parser.add_argument('result_images', help='over images.')

    args = parser.parse_args()
    base_images_format = args.base_images
    over_images_format = args.over_images
    result_images_format = args.result_images

    logger.debug(
        "base images format is {}, over images format is {}, result images format is {}.".format(
            base_images_format, over_images_format, result_images_format))

    base_images = Images(images_format=base_images_format)
    over_images = Images(images_format=over_images_format)

    over_images_iter = over_images.iter()

    # 默认result的num从1开始
    combine_num = 1

    for base_image in base_images.iter():
        try:
            over_image = over_images_iter.next()
        except StopIteration:
            # 如果发生 StopIteration 则意味着 over_images 迭代完了，需要进入下一次迭代。
            # 处理异常并且重新赋值
            over_images_iter = over_images.iter()
            over_image = over_images_iter.next()

        combine_images(base_image, over_image, result_images_format % combine_num)
        combine_num += 1


if __name__ == '__main__':
    main()
