# -*- coding: utf-8 -*-
from __future__ import absolute_import

__author__ = 'LibX'


class ThirdPartyBase(object):
    def __init__(self):
        pass

    def login(self):
        pass

    def porn_image(self, image_url):
        raise NotImplemented()

    def porn_images(self, image_urls):
        raise NotImplemented()

    def ocr_image(self, image_url):
        raise NotImplemented()

    def ocr_images(self, image_url):
        raise NotImplemented()


class ThirdPartyError(Exception):
    def __init__(self, *args, **kwargs):
        super(ThirdPartyError, self).__init__(*args, **kwargs)


class ThirdPartyHttpError(ThirdPartyError):
    def __init__(self, *args, **kwargs):
        self.status_code = kwargs.pop('status_code', None)
        self.content = kwargs.pop('content', None)
        super(ThirdPartyError, self).__init__(*args, **kwargs)

    def __setstate__(self, state):
        # for pickle
        self.status_code = state.get('status_code', None)
        self.content = state.get('content', None)


class ThirdPartyApiError(ThirdPartyError):
    def __init__(self, *args, **kwargs):
        self.err_no = kwargs.pop('err_no', None)
        self.err_msg = kwargs.pop('err_msg', None)

        if self.err_no and self.err_msg:
            exception_msg = 'API Error, err_no: %s, err_msg: %s' % (self.err_no, self.err_msg)
            super(ThirdPartyError, self).__init__(exception_msg)
        else:
            super(ThirdPartyError, self).__init__(*args, **kwargs)

    def __setstate__(self, state):
        # for pickle
        self.err_no = state.get('err_no', None)
        self.err_msg = state.get('err_msg', None)


class PornResult(object):
    def __init__(self, label, confidence, is_review, response=None, remark=None):
        self.label = label  # 1=正常,2=介于正常和色情之间,3=色情
        self.confidence = confidence  # 置信度
        self.is_review = is_review  # 0=不需要, 1=需要
        self.response = response
        self.remark = remark

    def __str__(self):
        return "Label:{}\tConfidence:{}\tis_review:{}".format(self.label, self.confidence, self.is_review)


class OCRResult(object):
    def __init__(self, items=list(), response=None):
        self.items = items
        self.response = response


class OCRItem(object):
    def __init__(self, text, confidence, position):
        self.text = text  # 文字内容
        self.confidence = confidence  # 置信度
        self.position = position  # 位置, 由于每个接口表示方式都不一致, 暂时不做转换

    def to_json(self):
        return {
            'text': self.text,
            'confidence': self.confidence,
            'position': self.position
        }
