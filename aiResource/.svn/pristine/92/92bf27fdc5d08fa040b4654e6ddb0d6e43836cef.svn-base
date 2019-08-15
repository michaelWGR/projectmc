# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import random
import datetime
# TODO rsa不支持PKCS8, 改用pycrypto
import rsa
import requests
import base64
import json
import types
from management.third_party.base import *

__author__ = 'LibX'

TUPU_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDyZneSY2eGnhKrArxaT6zswVH9
/EKz+CLD+38kJigWj5UaRB6dDUK9BR6YIv0M9vVQZED2650tVhS3BeX04vEFhThn
NrJguVPidufFpEh3AgdYDzOQxi06AN+CGzOXPaigTurBxZDIbdU+zmtr6a8bIBBj
WQ4v2JR/BA6gVHV5TwIDAQAB
-----END PUBLIC KEY-----
"""


class TUPU:
    def __init__(self, secret_id, private_key_path, url='http://api.open.tuputech.com/v3/recognition/'):
        self.__url = url + ('' if url.endswith('/') else '/') + secret_id
        self.__secret_id = secret_id
        # get private key
        with open(private_key_path) as private_key_file:
            self.__private_key = rsa.PrivateKey.load_pkcs1(private_key_file.read())
        # get tupu public key
        self.__public_key = rsa.PublicKey.load_pkcs1_openssl_pem(TUPU_PUBLIC_KEY)

    def __sign(self):
        """get the signature"""
        timestamp = datetime.datetime.now()
        nonce = random.randint(1 << 4, 1 << 32)
        sign_string = "%s,%s,%s" % (self.__secret_id, timestamp, nonce)
        signature = base64.b64encode(rsa.sign(sign_string.encode("utf-8"), self.__private_key, 'SHA-256'))

        return {
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature
        }

    def __verify(self, signature, verify_string):
        """verify the signature"""
        try:
            rsa.verify(verify_string.encode("utf-8"), base64.b64decode(signature), self.__public_key)
            return True
        except rsa.pkcs1.VerificationError:
            pass
        return False

    def api(self, images):
        request_data = self.__sign()
        request_data.update({
            "image": images
        })

        response = requests.post(self.__url, data=request_data)

        if response.status_code != 200:
            raise ThirdPartyHttpError('status code is not 200 but %d' % (response.status_code, ),
                                      status_code=response.status_code, content=response.text)

        response_json = response.json()
        if not self.__verify(response_json['signature'], response_json['json']):
            raise ThirdPartyError('verify response failed, signature=%s, json=%s' %
                                  (response_json['signature'], response_json['json']))

        response_json['json'] = json.loads(response_json['json'])
        if response_json['json']["code"] != 0:
            raise ThirdPartyApiError(err_no=response_json['json']["code"],
                                     err_msg=response_json["json"]["message"])
        return response_json


class TuPuCheck(ThirdPartyBase):
    OCR_TASK_ID = '578c7756fbbf7b8a6d92892a'

    def __init__(self, secret_id, private_key_path):
        super(TuPuCheck, self).__init__()
        self.__tupu_porn = TUPU(secret_id=secret_id["porn"], private_key_path=private_key_path)
        self.__tupu_ocr = TUPU(secret_id=secret_id["ocr"], private_key_path=private_key_path)

    @staticmethod
    def __make_porn_result(result):
        label_keyword = {"2": 1, "1": 2, "0": 3}
        porn_result = None
        for key, value in result["json"].items():
            if type(value) is types.DictType:
                for ret in value["fileList"]:
                    if str(ret["label"]) not in label_keyword:
                        raise ThirdPartyError(ret["label"] + "not definition")
                    label = label_keyword[str(ret["label"])]
                    confidence = ret["rate"]
                    if ret["review"]:
                        is_review = 1
                    else:
                        is_review = 0
                    porn_result = PornResult(label, confidence, is_review, response=result)
        return porn_result

    def porn_image(self, image_url):
        porn_result = self.__tupu_porn.api(images=[image_url, ])
        __porn_result = TuPuCheck.__make_porn_result(porn_result)
        if __porn_result:
            return __porn_result
        else:
            raise ThirdPartyError("get label error")

    @staticmethod
    def ___make_ocr_result(result):
        try:
            task_id = TuPuCheck.OCR_TASK_ID
            ocr_items = [
                OCRItem(text=item['text'], confidence=None, position=item['location'])
                for item in result['json'][task_id]['fileList'][0]['objects']
            ]
            return OCRResult(items=ocr_items, response=result)
        except ValueError, e1:
            raise ThirdPartyApiError('Response result is not json type!', e1)
        except KeyError, e2:
            raise ThirdPartyApiError(result['error_code'], result['error_msg'], e2)

    def ocr_image(self, image_url):
        ocr_result = self.__tupu_ocr.api(images=[image_url, ])
        return TuPuCheck.___make_ocr_result(ocr_result)


ThirdParty = TuPuCheck
