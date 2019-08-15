# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import time
import datetime
import random
import base64
import types
import urlparse
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

import requests
from management.third_party.base import ThirdPartyBase, ThirdPartyError, ThirdPartyHttpError, ThirdPartyApiError, \
    PornResult, OCRResult, OCRItem

__author__ = 'LibX'

# TODO 暂时没有公钥, 暂时留空
YY_PUBLIC_KEY = """
"""


class YYAiImageAPI(object):
    BASE_URL = 'http://api.aladdin.yy.com/v2/recognition/'

    def __init__(self, secret_id, private_key_path):
        self.__url = urlparse.urljoin(YYAiImageAPI.BASE_URL, '/'.join((secret_id, 'url', '')))
        self.__secret_id = secret_id
        # get private key
        with open(private_key_path) as private_key_file:
            self.__private_key = RSA.import_key(private_key_file.read())
        self.__signer = PKCS1_v1_5.new(self.__private_key)

        # get yy public key
        # TODO 暂时没有公钥, 暂时留空
        self.__public_key = None  # rsa.PublicKey.load_pkcs1_openssl_pem(YY_PUBLIC_KEY)

    def __sign(self):
        """get the signature"""
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        nonce = random.random()  # random.randint(1 << 4, 1 << 32)
        sign_string = "%s,%s,%s" % (self.__secret_id, timestamp, nonce)

        # signature = base64.b64encode(rsa.sign(sign_string.encode("utf-8"), self.__private_key, 'SHA-256'))

        digest = SHA256.new()
        digest.update(sign_string.encode("utf-8"))
        signature = base64.b64encode(self.__signer.sign(digest))

        return {
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature
        }

    def __verify(self, signature, verify_string):
        """verify the signature"""
        # try:
        #     rsa.verify(verify_string.encode("utf-8"), base64.b64decode(signature), self.__public_key)
        #     return True
        # except rsa.pkcs1.VerificationError:
        #     pass
        # return False
        # TODO 暂时没有公钥, 暂时留空
        return True

    def request(self, task_id, images):
        request_data = self.__sign()
        request_data.update({
            'taskId': task_id,
            'image': images
        })

        response = requests.post(self.__url, data=request_data)

        if response.status_code != 200:
            raise ThirdPartyHttpError('status code is not 200 but %d' % (response.status_code,),
                                      status_code=response.status_code, content=response.text)

        response_json = response.json()
        if not self.__verify(response_json['signature'], response_json['json']):
            raise ThirdPartyError('verify response failed, signature=%s, json=%s' %
                                  (response_json['signature'], response_json['json']))

        response_json['json'] = json.loads(response_json['json'])
        if response_json['json']["code"] != '0':
            raise ThirdPartyApiError(err_no=response_json['json']["code"],
                                     err_msg=response_json["json"]["message"])
        return response_json


class YYAiImage(ThirdPartyBase):
    PORN_TASK_ID = '64bcfc6c329af61034f8c2f6'
    OCR_TASK_ID = '65bcfc6c329af61034f8c2f2'
    REAL_LABELS_MAPPING = {'normal': 1, 'sexy': 2, 'porn': 3, 'exposed': 4, 'wrestling': 5}
    LABELS_MAPPING = {'normal': 1, 'others': 2, 'porn': 3}
    LABEL_OTHERS = 'others'

    def __init__(self, secret_id, private_key_path):
        super(YYAiImage, self).__init__()
        self.__api = YYAiImageAPI(secret_id=secret_id, private_key_path=private_key_path)

    def porn_image(self, image_url):
        response_json = self.__api.request(task_id=YYAiImage.PORN_TASK_ID, images=[image_url, ])
        porn_result_json = response_json['json']['filelist'][0][YYAiImage.PORN_TASK_ID]
        real_label = porn_result_json['label']
        label = real_label if real_label in YYAiImage.LABELS_MAPPING.keys() else YYAiImage.LABEL_OTHERS
        return PornResult(label=YYAiImage.LABELS_MAPPING[label],
                          confidence=porn_result_json['rate'],
                          is_review=porn_result_json['review'],
                          response=response_json,
                          remark=YYAiImage.REAL_LABELS_MAPPING[real_label])

    def ocr_image(self, image_url):
        response_json = self.__api.request(task_id=YYAiImage.OCR_TASK_ID, images=[image_url, ])
        ocr_items = [
            OCRItem(text=ocr_file_json[YYAiImage.OCR_TASK_ID]['ext_data']['text'],
                    confidence=ocr_file_json[YYAiImage.OCR_TASK_ID]['rate'],
                    position=None)
            for ocr_file_json in response_json['json']['filelist']
            ]
        return OCRResult(items=ocr_items, response=response_json)


ThirdParty = YYAiImage
