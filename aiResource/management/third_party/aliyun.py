# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
import json
import uuid

'''
pip install aliyun-python-sdk-core==2.8.2
pip install -v aliyun-python-sdk-green==3.2.0
'''
from management.third_party.base import *
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import ImageSyncScanRequest
import requests

__author__ = 'LibX'


class Aliyun(ThirdPartyBase):
    OCR_URL = 'https://ocrapi-ecommerce.taobao.com/ocrservice/ecommerce'
    APPCODE = '746d581b145b4c7591dc14a9071deb20'

    def __init__(self, access_key_id, access_key_secret, domain, server):
        super(Aliyun, self).__init__()
        self.__clt = client.AcsClient(access_key_id, access_key_secret,
                                      server)
        region_provider.modify_point('Green', server, domain)

    @staticmethod
    def __make_result(scene_result, result):
        label_keyword = {"normal": 1, "sexy": 2, "porn": 3}
        suggestion_keyword = {"pass": 0, "review": 1, "block": 0}
        if scene_result["label"] in label_keyword:
            label = label_keyword[scene_result["label"]]
        else:
            raise ThirdPartyError(scene_result["label"] + "not definition")
        if scene_result["suggestion"] in suggestion_keyword:
            is_review = suggestion_keyword[scene_result["suggestion"]]
        else:
            raise ThirdPartyError(scene_result["suggestion"] + "not definition")
        confidence = scene_result["rate"] / float(100)
        return PornResult(label, confidence, is_review, response=result)

    def porn_image(self, image_url):
        scene = "porn"
        request = ImageSyncScanRequest.ImageSyncScanRequest()
        request.set_accept_format('JSON')

        task = {"dataId": str(uuid.uuid1()),
                "url": image_url,
                "time": datetime.datetime.now().microsecond
                }

        request.set_content(bytearray(json.dumps({"tasks": [task], "scenes": [scene]}), "utf-8"))
        response = self.__clt.do_action_with_exception(request)
        result = json.loads(response)
        if 200 == result["code"]:
            task_results = result["data"]
            for taskResult in task_results:
                if 200 == taskResult["code"]:
                    scene_results = taskResult["results"]
                    for sceneResult in scene_results:
                        return Aliyun.__make_result(sceneResult, result)

                else:
                    raise ThirdPartyApiError(err_no=taskResult["code"], err_msg=taskResult["msg"])
        else:
            raise ThirdPartyApiError(err_no=result["code"], err_msg=result["msg"])

    def ocr_image(self, image_url):

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'APPCODE ' + Aliyun.APPCODE,
        }
        datas = '{"url": "%s", "prob": true}' % image_url
        try:
            response = requests.post(Aliyun.OCR_URL, headers=headers, data=datas, verify=False)
        except Exception, e:
            raise ThirdPartyHttpError(e)
        if response.status_code == 200:
            try:
                results = response.json()
                ocr_items = [
                    OCRItem(text=item['word'], confidence=item['prob'], position=item['pos'])
                    for item in results['prism_wordsInfo']
                ]
                return OCRResult(items=ocr_items, response=response.text)
            except ValueError, e1:
                raise ThirdPartyApiError('Response result is not json type!')
            except KeyError, e2:
                raise ThirdPartyApiError(results['error_code'], results['error_msg'])
        else:
            raise ThirdPartyHttpError('status code is not 200 but %d' % (response.status_code, ),
                                      response.status_code, response.content)


ThirdParty = Aliyun
