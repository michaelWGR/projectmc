# -*- coding:utf-8 -*-
import requests
import base64, hmac, hashlib
import time, random, os


class TencentApi(object):
    _APP_ID = '1257170265'
    _SECRET_ID = 'AKIDBLTUN88KmFZizBeyb6Rj5gKbieRq9W1O'
    _SECRET_KEY = 'Ut7B6DF6pMk2FPSK6lIetzwlQ8vrlaHr'

    def __init__(self, url, app_id=None, secret_id=None, secret_key=None):
        self.url = url
        self.app_id = app_id if app_id else self._APP_ID
        self.secret_id = secret_id if secret_id else self._SECRET_ID
        self.secret_key = secret_key if secret_key else self._SECRET_KEY
        self.authorization = self._get_authorized_sign()

    def _get_authorized_sign(self):
        orignal = 'a={}&k={}&e={}&t={}&r={}'.format(self.app_id, self.secret_id, int(time.time()) + 3600 * 24 * 90,
                                                    int(time.time()), random.randint(1, 100))
        sign = hmac.new(self.secret_key, orignal, hashlib.sha1).digest()
        return base64.standard_b64encode(sign + orignal)

    def request_result(self, file_paths):
        raise NotImplementedError('Must override this method!')


class TencentPorn(TencentApi):
    _URL = 'http://service.image.myqcloud.com/detection/porn_detect'

    def __init__(self, url=None, app_id=None, secret_id=None, secret_key=None):
        TencentApi.__init__(self, url if url else self._URL, app_id, secret_id, secret_key)

    def request_result(self, file_paths):
        files = {
            'appid': self.app_id
        }
        for i in range(len(file_paths)):
            file_name = os.path.basename(file_paths[i])
            files['image[{}]'.format(i)] = (file_name, open(file_paths[i], 'rb'), "image/jpeg")

        headers = {
            'authorization': self.authorization,
        }

        try:
            response = requests.post(self.url, headers=headers, files=files)
            if response.status_code == 200:
                try:
                    results = response.json()
                    results_list = results['result_list']
                    for result in results_list:
                        print result['data']
                except Exception, e:
                    raise RuntimeError('Result type is not json or json key is wrong!,{}'.format(e))
            else:
                raise RuntimeError('Tencent porn api requests failed, cause:{}'.format(response.text))
        except Exception, e:
            print e


class TencentOCR(TencentApi):
    _URL = 'http://recognition.image.myqcloud.com/ocr/general'

    def __init__(self, url=None, app_id=None, secret_id=None, secret_key=None):
        TencentApi.__init__(self, url if url else self._URL, app_id, secret_id, secret_key)

    def request_result(self, file_path):
        files = {
            'appid': self.app_id,
            'image': (os.path.basename(file_path), open(file_path, 'rb'), "image/jpeg")
        }
        headers = {
            'authorization': self.authorization,
        }
        try:
            response = requests.post(self.url, headers=headers, files=files)
            if response.status_code == 200:
                try:
                    results = response.json()
                    for item in results['data']['items']:
                        print item['itemstring']
                except Exception, e:
                    raise RuntimeError('Result type is not json or json key is wrong!,{}'.format(e))
            else:
                raise RuntimeError('Tencent ocr api requests failed, cause:{}'.format(response.text))
        except Exception, e:
            print e


if __name__ == '__main__':
    files = ['/Users/yyinc/Downloads/IMG_1080.JPG']
    TencentPorn().request_result(files)
