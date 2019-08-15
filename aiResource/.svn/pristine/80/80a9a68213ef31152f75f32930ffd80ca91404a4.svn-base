# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.core.management import BaseCommand

from management.models import Resource
from management.third_party import ThirdPartyManager
from management.utils.sample_runner import SampleRunner

__author__ = 'LibX'


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument('business_type', help='porn, ocr')
        parser.add_argument('products')
        parser.add_argument('resource_id', type=int)

    def handle(self, *args, **options):
        business_type = options.get('business_type')

        products = options.get('products', None)
        product_names = [s.strip() for s in products.split(',') if s.strip()]

        from django.conf import settings
        third_parties = dict(
            (product_name, ThirdPartyManager.get_third_party(settings, product_name)) for product_name in product_names
        )

        for third_party in third_parties.values():
            third_party.login()

        runners = dict(
            (product_name, SampleRunner(product_name, third_party, business_type, logger=logger))
            for product_name, third_party in third_parties.items()
        )

        resource_id = options.get('resource_id')

        try:
            resource = Resource.objects.get(id=resource_id)
            for third_party_name, runner in runners.items():
                try:
                    runner.run(resource)
                except Exception:
                    logger.exception('run resource id %d error', resource_id)
        except (Resource.DoesNotExist, Resource.MultipleObjectsReturned) as e:
            logger.exception('resource id %d error', resource_id)
