# -*- coding: utf-8 -*-
from __future__ import absolute_import

import csv
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
        parser.add_argument('--dry-run', action='store_true', default=False, help='dry run')
        parser.add_argument('--just-error', action='store_true', default=False, help='just error')
        parser.add_argument('business_type', help='porn, ocr')
        parser.add_argument('products')
        parser.add_argument('resource_csv_path')

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        just_error = options.get('just_error', False)

        business_type = options.get('business_type')

        products = options.get('products', None)
        product_names = [s.strip() for s in products.split(',') if s.strip()]

        from django.conf import settings
        third_parties = dict(
            (product_name, ThirdPartyManager.get_third_party(settings, product_name)) for product_name in product_names
        )

        for third_party in third_parties.values():
            third_party.login()

        runner_options = {
            'logger': logger,
            'dry_run': dry_run,
            'just_error': just_error
        }
        runners = dict(
            (product_name, SampleRunner(product_name, third_party, business_type, **runner_options))
            for product_name, third_party in third_parties.items()
        )

        resource_csv_path = options.get('resource_csv_path', None)
        with open(resource_csv_path, 'rb') as resource_csv_file:
            resource_csv_reader = csv.reader(resource_csv_file)

            for row in resource_csv_reader:
                if not row:
                    # ignore empty row
                    continue
                try:
                    resource_id = int(row[0])
                except ValueError as e:
                    logger.exception('invalid resource id %s', row[0])
                    continue

                try:
                    resource = Resource.objects.get(id=resource_id)
                except (Resource.DoesNotExist, Resource.MultipleObjectsReturned) as e:
                    logger.exception('resource id %d error', resource_id)
                    continue

                for third_party_name, runner in runners.items():
                    try:
                        runner.run(resource)
                    except Exception:
                        logger.exception('run resource id %d error', resource_id)
