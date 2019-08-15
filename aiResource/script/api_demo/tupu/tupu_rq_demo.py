# -*- coding:utf-8 -*-
from tupu_api import TUPU
import pprint

"""
    色情识别Secret-ID:5b582d8393c70fabecff93a7
    鉴黄
    label值  名称
    0	色情
    1	性感
    2	正常

    广告文字识别Secret-ID:5b5aca05878b01abf107e3c9
    广告文字识别
    label值  名称
    0       无文字
    1       二维码
    2       带文字图片
    返回值：
    text——图片中识别出来的文字信息
    location——图片中所识别出来的文字句子的位置
    label——识别图片的类别

    更详细参数返回查看 demo 返回值

"""


def main():
    tupu_porn = TUPU(secret_id='5b582d8393c70fabecff93a7', private_key_path='./tupu_rsa_private_key.pem')
    tupu_ocr = TUPU(secret_id='5b5aca05878b01abf107e3c9', private_key_path='./tupu_rsa_private_key.pem')

    # url
    # images = ["http://example.com/001.jpg", "http://example.com/002.jpg"]
    # result = tupu.api(images=images, is_url=True)

    # image file
    ocr_images = ["../ad_ocr.jpg"]
    ocr_result = tupu_ocr.api(images=ocr_images, is_url=False)
    print pprint.pprint(ocr_result)

    porn_images = ["../porn.jpg", "../not_porn.jpg"]
    porn_result = tupu_porn.api(images=porn_images, is_url=False)
    print pprint.pprint(porn_result)

    # zip file
    # images = ["/home/user/001.zip", "/home/user/002.zip"]
    # result = tupu.api(images=images, is_url=False)




if __name__ == '__main__':
    main()
