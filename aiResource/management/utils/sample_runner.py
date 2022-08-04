# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging
from management.utils import traceback_ex
from urlparse import urlparse, urlunparse

from management.third_party.base import PornResult, OCRResult, OCRItem
from management.models import PornResult as DBPornResult, OCRResult as DBOCRResult

__author__ = 'LibX'

__logger__ = logging.getLogger(__name__)


def get_internet_resource_path(path):
    res_url_parsed = urlparse(path.strip())

    res_url_splits = list(res_url_parsed)
    res_url_splits[1] = '122.13.200.245:7070'
    return urlunparse(res_url_splits)


class PornAdapter(object):
    def __init__(self):
        pass

    def get_defaults(self):
        return {
            'label': 0,
            'rate': 0.0,
            'is_review': 0,
            'is_error': 0,
            'errors': None,
            'remark': None
        }

    def run_by_url(self, third_party, url):
        return third_party.porn_image(url)

    def update_defaults(self, defaults, result):
        defaults.update({
            'label': result.label,
            'rate': result.confidence,
            'is_review': result.is_review,
            'remark': result.remark
        })

    def get_db_result_model(self):
        return DBPornResult

    def is_error_result(self, third_party, resource_id):
        try:
            print(third_party, resource_id)
            result = DBPornResult.objects.get(product=third_party, resource=resource_id)
            return result.is_error != 0
        except DBPornResult.DoesNotExist as e:
            # not run
            return False


class OCRAdapter(object):
    def __init__(self):
        pass

    def get_defaults(self):
        return {
            'items': None,
            'is_error': 0,
            'errors': None,
            'remark': None
        }

    def run_by_url(self, third_party, url):
        return third_party.ocr_image(url)

    def update_defaults(self, defaults, result):
        defaults.update({
            'items': json.dumps([item.to_json() for item in result.items])
        })

    def get_db_result_model(self):
        return DBOCRResult

    def is_error_result(self, third_party, resource_id):
        try:
            result = DBOCRResult.objects.get(product=third_party, resource=resource_id)
            return result.is_error != 0
        except DBPornResult.DoesNotExist as e:
            # not run
            return False


business_adapters = {
    'porn': PornAdapter(),
    'ocr': OCRAdapter()
}


class SampleRunner(object):
    def __init__(self, third_party_name, third_party, business_type, **kwargs):
        self.third_party_name = third_party_name
        self.third_party = third_party
        self.business_type = business_type
        self.business_adapter = SampleRunner.get_business_adapter(business_type)

        # options
        self.logger = kwargs.pop('logger', __logger__)
        self.dry_run = kwargs.pop('dry_run', False)
        self.just_error = kwargs.pop('just_error', False)

    @classmethod
    def get_business_adapter(cls, business_type):
        if business_type not in business_type:
            raise ValueError('invalid business type %s' % (business_type,))
        return business_adapters.get(business_type)

    def is_error_result(self, resource_id):
        return self.business_adapter.is_error_result(self.third_party_name, resource_id)

    def run(self, resource):
        if self.just_error and not self.is_error_result(resource.id):
            self.logger.info('ignore non-error %s result resource id %d, product %s',
                             self.business_type, resource.id, self.third_party_name)
            return

        defaults = self.business_adapter.get_defaults()
        try:
            self.logger.info('%s resource id %d with product %s', self.business_type, resource.id,
                             self.third_party_name)
            image_url = get_internet_resource_path(resource.path)
            third_party_result = self.business_adapter.run_by_url(self.third_party, image_url)

            self.business_adapter.update_defaults(defaults, third_party_result)
        except Exception as e:
            self.logger.exception('porn error')

            defaults.update({
                'is_error': 1,
                'errors': json.dumps(traceback_ex.json_exc()),
            })

        if self.dry_run:
            return

        try:
            db_result_model = self.business_adapter.get_db_result_model()
            porn_result, created = db_result_model.objects.update_or_create(
                resource_id=resource.id,
                product=self.third_party_name,
                defaults=defaults
            )

            action = 'create' if created else 'update'
            self.logger.info('%s %s result resource id %d, product %s',
                             action, self.business_type, resource.id, self.third_party_name)
            # if porn_result.is_error:
            #     logger.error('%s result id %d, is_error %d, errors %s',
            #                  business_type, porn_result.id, porn_result.is_error, json.loads(porn_result.errors))
            # else:
            #     logger.info('%s result id %d, label %d, rate %.2f, is_review %d',
            #                 business_type, porn_result.id, porn_result.label, porn_result.rate, porn_result.is_review)

            return
        except Exception as e:
            self.logger.exception('update or create %s result error', self.business_type)
