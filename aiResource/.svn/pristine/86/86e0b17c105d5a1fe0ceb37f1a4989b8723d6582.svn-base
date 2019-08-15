# -*- coding: utf-8 -*-
from __future__ import absolute_import


import os
import copy
import pkgutil


__author__ = 'LibX'


class ThirdPartyManager(object):
    _cache = None

    def __init__(self):
        raise ValueError()

    @classmethod
    def _get_third_party_modules(cls):
        third_party_path = os.path.dirname(os.path.abspath(__file__))

        for module_loader, module_name, is_pkg in pkgutil.iter_modules([third_party_path, ]):
            if is_pkg:
                continue

            if module_name == 'base':
                continue

            abs_module_name = 'management.third_party.' + module_name
            yield module_name, abs_module_name

    @classmethod
    def get_third_party_modules(cls):
        if cls._cache is None:
            cls._cache = dict(cls._get_third_party_modules())
        return copy.deepcopy(cls._cache)

    @classmethod
    def get_third_party_class(cls, name):
        third_party_modules = cls.get_third_party_modules()
        if name not in third_party_modules:
            raise ValueError('third_party %s is not registry.' % (name, ))

        abs_module_name = third_party_modules.get(name)
        module = __import__(abs_module_name, fromlist=[abs_module_name, ])

        return getattr(module, 'ThirdParty')

    @classmethod
    def get_third_party_setting(cls, settings, name):
        setting_key = '%s_SETTING' % (name.upper(), )
        return getattr(settings, setting_key, None)

    @classmethod
    def get_third_party(cls, settings, name):
        third_party_class = cls.get_third_party_class(name)
        third_party_setting = cls.get_third_party_setting(settings, name)
        return third_party_class(**third_party_setting)
