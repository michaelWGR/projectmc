# -*- coding: utf-8 -*-
from __future__ import absolute_import
from management.third_party.base import ThirdPartyBase, ThirdPartyHttpError, ThirdPartyApiError, OCRResult, OCRItem
import requests

__author__ = 'LSH'


class BaiduCloud(ThirdPartyBase):
    OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage'

    def __init__(self, app_id, secret_id, secret_key):
        ThirdPartyBase.__init__(self)
        self.app_id = app_id
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.access_token = None

    def login(self):
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            self.secret_id, self.secret_key)

        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        try:
            response = requests.post(host, headers=headers)
        except Exception, e:
            raise ThirdPartyHttpError(e)
        if response.status_code == 200:
            try:
                results = response.json()
                return results['access_token']
            except ValueError, e1:
                raise ThirdPartyApiError('Response result is not json type!',e1)
            except KeyError, e2:
                raise ThirdPartyApiError(results['error_code'], results['error_msg'], e2)
        else:
            raise ThirdPartyHttpError('status code is not 200 but %d' % (response.status_code, ),
                                      response.status_code, response.content)

    def ocr_image(self, image_url):
        if not self.access_token:
            self.login()
        datas = {
            'access_token': self.access_token,
            'url': image_url
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        try:
            response = requests.post(BaiduCloud.OCR_URL, headers=headers, data=datas)
        except Exception, e:
            raise ThirdPartyHttpError(e)
        if response.status_code == 200:
            try:
                results = response.json()
                ocr_items = [
                    OCRItem(text=item['words'], confidence=None, position=None)
                    for item in results['words_result']
                ]
                return OCRResult(items=ocr_items, response=response.text)
            except ValueError, e1:
                raise ThirdPartyApiError('Response result is not json type!', e1)
            except KeyError, e2:
                raise ThirdPartyApiError(results['error_code'], results['error_msg'], e2)
        else:
            raise ThirdPartyHttpError('status code is not 200 but %d' % (response.status_code, ),
                                      response.status_code, response.content)


ThirdParty = BaiduCloud
