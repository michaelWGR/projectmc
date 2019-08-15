# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

import json
import hashlib
import hmac

import requests
from management.third_party.base import ThirdPartyBase, ThirdPartyError, ThirdPartyHttpError, ThirdPartyApiError, PornResult


__author__ = 'LibX'


# 继承ThirdPartyBase实现, 请按照命名规范命名类名
class KSYun(ThirdPartyBase):
    CURRENT_VERSION = '2017-11-07'

    def __init__(self, access_key, secret_key):
        # 每个服务需要的鉴定参数不一定一样, 请自行定义
        super(KSYun, self).__init__()
        self.access_key = access_key
        self.secret_key = secret_key
        self.version = KSYun.CURRENT_VERSION

    @staticmethod
    def sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    @staticmethod
    def getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = KSYun.sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = KSYun.sign(kDate, regionName)
        kService = KSYun.sign(kRegion, serviceName)
        kSigning = KSYun.sign(kService, 'aws4_request')
        return kSigning

    @staticmethod
    def encode(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    def request(self, action, post_body):
        # 根据http://ai.ksyun.com/techapi的example改写

        method = 'POST'
        service = 'kir'
        host = 'kir.api.ksyun.com'
        region = 'cn-beijing-6'
        endpoint = 'http://kir.api.ksyun.com/'
        contenttype = 'application/json'
        request_parameters = 'Action=%s&Version=%s' % (action, self.version, )

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope
        #amzdate = '20171129T100303Z'
        #datestamp = '20171129'

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************

        # Step 1 is to define the verb (GET, POST, etc.)--already done.

        # Step 2: Create canonical URI--the part of the URI from domain to query
        # string (use '/' if no path)
        canonical_uri = '/'

        # Step 3: Create the canonical query string. In this example (a GET request),
        # request parameters are in the query string. Query string values must
        # be URL-encoded (space=%20). The parameters must be sorted by name.
        # For this example, the query string is pre-formatted in the request_parameters variable.
        canonical_querystring = request_parameters

        # Step 4: Create the canonical headers and signed headers. Header names
        # must be trimmed and lowercase, and sorted in code point order from
        # low to high. Note that there is a trailing \n.
        canonical_headers = 'content-type:' + contenttype + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'

        # Step 5: Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the
        # hash of the request. "Host" and "x-amz-date" are always required.
        signed_headers = 'content-type;host;x-amz-date'

        # Step 6: Create payload hash (hash of the request body content). For GET
        # requests, the payload is an empty string ("").
        payload_hash = hashlib.sha256(post_body).hexdigest()

        # Step 7: Combine elements to create canonical request
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signing_key = self.getSignatureKey(self.secret_key, datestamp, region, service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        # The signing information can be either in a query string value or in
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        authorization_header = algorithm + ' ' + 'Credential=' + self.access_key + '/' + credential_scope + ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

        # The request can include any headers, but MUST include "host", "x-amz-date",
        # and (for this scenario) "Authorization". "host" and "x-amz-date" must
        # be included in the canonical_headers and signed_headers, as noted
        # earlier. Order here is not significant.
        # Python note: The 'host' header is added automatically by the Python 'requests' library.
        headers = {'Content-Type': "application/json", 'X-Amz-Date': amzdate, 'Authorization': authorization_header}

        # ************* SEND THE REQUEST *************
        request_url = endpoint + '?' + canonical_querystring

        # print '[%s]' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ), 'do request', post_body
        resp = requests.request("POST", request_url, data=post_body, headers=headers, verify=False)
        if resp.status_code != 200:
            try:
                content = resp.text
            except Exception as e:
                content = ''
            raise ThirdPartyHttpError('status code is not 200 but %d' % (resp.status_code, ),
                                      status_code=resp.status_code, content=content)

        resp_json = resp.json()
        resp_json_header = resp_json.get('header', None)
        if not resp_json_header:
            raise ThirdPartyError('invalid response format')

        err_no = resp_json_header.get('err_no', None)
        err_msg = self.encode(resp_json_header.get('err_msg', ''))
        if err_no is None:
            raise ThirdPartyError('invalid response format')

        if err_no != 200:
            raise ThirdPartyApiError(err_no=err_no, err_msg=err_msg)

        return resp_json

    def classify_image(self, business, image_urls):
        post_body = json.dumps(
            {
                "business": business,
                "image_urls": image_urls
            }

        )
        return self.request('ClassifyImage', post_body)

    def porn_image(self, image_url):
        # 先实现单图业务
        resp_json = self.classify_image(['porn'], (image_url,))

        resp_body = resp_json.get('body', None)
        if not resp_body:
            raise ThirdPartyError('response body is empty')

        resp_body = resp_body[0]
        if 'err_no' in resp_body:
            err_no = resp_body['err_no']
            err_msg = KSYun.encode(resp_body['err_msg'])
            raise ThirdPartyApiError(err_no=err_no, err_msg=err_msg)

        resp_results = resp_body.get('results', None)
        if not resp_results:
            raise ValueError('response has no result')

        porn_result_json = resp_results[0]
        if 'err_no' in porn_result_json:
            err_no = porn_result_json['err_no']
            err_msg = KSYun.encode(porn_result_json['err_msg'])
            raise ThirdPartyApiError(err_no=err_no, err_msg=err_msg)

        label = int(porn_result_json['label'])
        rate = porn_result_json['rate']
        is_review = porn_result_json['review']

        return PornResult(label, rate, is_review)


# 必须声明, 提供给commands进行动态获取
ThirdParty = KSYun
