# -*- coding:utf-8 -*-
from __future__ import absolute_import

import datetime

from django.forms.utils import ErrorDict
from django.http import HttpResponse
from django.http import HttpRequest, JsonResponse
from django.http import HttpResponseNotAllowed


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.strftime('%Y-%m-%d %H:%M:%S')
        return serial

    raise TypeError("Type %s not serializable" % (type(obj),))


class JsonApiResponse(JsonResponse):
    def __init__(self, code, msg, result=None, errors=None):
        json_dict = {'code': code, 'msg': msg}
        if result is not None:
            json_dict['result'] = result
        if errors is not None:
            json_dict['errors'] = errors

        super(JsonApiResponse, self).__init__(json_dict, json_dumps_params={'default': json_serial})


class JsonApi(object):
    def __init__(self, logger=None, permitted_methods=('GET', 'POST')):
        self.logger = logger
        self.permitted_methods = permitted_methods

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            request = args[0]
            if isinstance(request, HttpRequest) and request.method not in self.permitted_methods:
                return HttpResponseNotAllowed(self.permitted_methods)

            try:
                ret = func(*args, **kwargs)
                return ret
            except Exception as e:
                if self.logger is not None:
                    self.logger.exception(e.message)
                msg = 'Unexpect exception: %s' % (e.message if e.message else '',)
                return JsonApiResponse(-1, msg)

        return wrapper


def main():
    pass


if __name__ == '__main__':
    main()
