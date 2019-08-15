# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import traceback


__author__ = 'LibX'


def json_exc(limit=None):
    try:
        etype, value, tb = sys.exc_info()
        return {
            'exception_class': etype.__name__,
            'message': unicode(value),
            'trace': ''.join(traceback.format_exception(etype, value, tb, limit))
        }
    finally:
        etype = value = tb = None
