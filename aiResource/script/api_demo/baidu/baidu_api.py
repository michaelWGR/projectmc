# -*- coding:utf-8 -*-
import requests
import base64

class BaiduApi(object):
    _APP_ID = '11612348'
    _SECRET_ID = '8wQ9G53im8RgZTebibkLsLg6'
    _SECRET_KEY = 'YHrtk3LBbqox5TMQjCCwkCr31XnhjpHv'

    def __init__(self, url, app_id=None, secret_id=None, secret_key=None):
        self.url = url
        self.app_id = app_id if app_id else self._APP_ID
        self.secret_id = secret_id if secret_id else self._SECRET_ID
        self.secret_key = secret_key if secret_key else self._SECRET_KEY
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            self.secret_id, self.secret_key)

        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        try:
            response = requests.post(host, headers=headers)
            if response.status_code == 200:
                try:
                    results = response.json()
                    return results['access_token']
                except Exception, e:
                    raise RuntimeError('Result type is not json or json key is wrong!,{}'.format(e))
            else:
                raise RuntimeError('Baidu ocr api requests failed, cause:{}'.format(response.text))
        except Exception, e:
            print e

    def request_result(self, file_paths):
        raise NotImplementedError('Must override this method!')


class BaiduOCR(BaiduApi):
    _URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage'

    def __init__(self, url=None, app_id=None, secret_id=None, secret_key=None):
        BaiduApi.__init__(self, url if url else self._URL, app_id, secret_id, secret_key)

    def request_result(self, file_path):
        files = {
            'access_token': self.access_token,
            'image': base64.b64encode(open(file_path, 'rb').read())
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        try:
            response = requests.post(self.url, headers=headers, data=files)
            if response.status_code == 200:
                try:
                    results = response.json()
                    for item in results['words_result']:
                        print item['words']
                except Exception, e:
                    raise RuntimeError('Result type is not json or json key is wrong!,{}'.format(e))
            else:
                raise RuntimeError('Tencent ocr api requests failed, cause:{}'.format(response.text))
        except Exception, e:
            print e


if __name__ == '__main__':
    files = '/Users/yyinc/Downloads/adv/1.jpg'
    BaiduOCR().request_result(files)
