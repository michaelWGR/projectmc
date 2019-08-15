# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time
import random
import hashlib
import json
import hmac
import base64
import requests
from management.third_party.base import ThirdPartyBase, ThirdPartyHttpError, ThirdPartyError, ThirdPartyApiError, \
    OCRItem, OCRResult, PornResult

__author__ = 'tommy'


class TXCloud(ThirdPartyBase):
    OCR_URL = 'http://recognition.image.myqcloud.com/ocr/general'
    PORN_URL = 'http://service.image.myqcloud.com/detection/porn_detect'

    def __init__(self, app_id, secret_id, secret_key):
        super(TXCloud, self).__init__()
        self.app_id = app_id
        self.secret_id = secret_id
        self.secret_key = secret_key

    def get_authorized_sign(self):
        orignal = 'a={}&k={}&e={}&t={}&r={}'.format(self.app_id, self.secret_id, int(time.time()) + 3600 * 24 * 90,
                                                    int(time.time()), random.randint(1, 100))
        sign = hmac.new(self.secret_key, orignal, hashlib.sha1).digest()
        return base64.standard_b64encode(sign + orignal)

    def request(self, image_url, _type="ocr"):
        response = None
        files = {'appid': self.app_id}
        if _type == "ocr":
            files['url'] = image_url
        elif _type == "porn":
            files['url_list'] = [image_url]

        headers = {
            'authorization': self.get_authorized_sign(),
        }
        if _type == "ocr":
            response = requests.post(TXCloud.OCR_URL, headers=headers, files=files)
        elif _type == "porn":
            response = requests.post(TXCloud.PORN_URL, headers=headers, data=json.dumps(files))
        if response.status_code != 200:
            try:
                content = response.text
            except Exception as e:
                content = ''
            raise ThirdPartyHttpError('status code is not 200 but %d' % (response.status_code,),
                                      status_code=response.status_code, content=content)
        resp_json = response.json()

        if not resp_json:
            raise ThirdPartyError('No data responsed')
        if _type == "ocr":
            err_no = resp_json.get('code', None)
            err_msg = resp_json.get('message', '')

            if err_no != 0:
                raise ThirdPartyApiError(err_no=err_no, err_msg=err_msg)
        else:
            for item in resp_json["result_list"]:
                err_no = item.get('code', None)
                err_msg = item.get('message', '')
                if err_no != 0:
                    raise ThirdPartyApiError(err_no=err_no, err_msg=err_msg)

        return resp_json

    def ocr_image(self, image_url):
        response = self.request(image_url)
        item_list = response['data']['items']
        ocr_items = [
            OCRItem(text=item['itemstring'], confidence=None, position=item['itemcoord'])
            for item in item_list
        ]
        return OCRResult(ocr_items, response)

    def porn_image(self, image_url):
        label_keyword = {"0": 1, "2": 2, "1": 3}
        porn_result = None
        results = self.request(image_url, _type="porn")
        if "result_list" in results:
            for result in results["result_list"]:
                if "data" in result:
                    try:
                        confidence = result["data"]['confidence'] / float(100)
                        if str(result["data"]['result']) not in label_keyword:
                            raise ThirdPartyError("get label error")
                        label = label_keyword[str(result["data"]['result'])]
                        porn_result = PornResult(label, confidence, 0, results)
                    except KeyError as e:
                        raise ThirdPartyError(e)
        if porn_result:
            return porn_result
        else:
            raise ThirdPartyError("get label error")


ThirdParty = TXCloud
