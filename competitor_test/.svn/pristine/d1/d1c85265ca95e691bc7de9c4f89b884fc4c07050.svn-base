# /usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import requests
import csv
import json

APP_DICT = {
    'hlwolf': '77',
    'fjwolf': '78',
    'ttwolf': '79',
    'wolf': '80',
    'yyshy': '81',
    'hyassist': '83',
    'hlwolfdev': '85',
    'hello': '87',
    'tt': '88',
}

CASE_DICT = {
    'mos': {
        '3_4_max': 278,
        '3_4_min': 279,
        '3_4_avg': 280,
        '3_4_std': 281,
        '4_3_max': 282,
        '4_3_min': 283,
        '4_3_avg': 284,
        '4_3_std': 285,
    },
    'delay': {
        '3_4_max': 286,
        '3_4_min': 287,
        '3_4_avg': 288,
        '3_4_std': 289,
        '4_3_max': 290,
        '4_3_min': 291,
        '4_3_avg': 292,
        '4_3_std': 293,
    }
}

ORDER_DICT = {
    '24': '1',
    '5': '2'
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('suite_id', type=int)
    parser.add_argument('type', choices=['mos', 'delay'])
    parser.add_argument('csv_path')
    args = parser.parse_args()

    print('suite_id: %d, type: %s, %s' %
          (args.suite_id, args.type, args.csv_path))

    commit_url = 'http://results.yypm.com/management/result/grid/%d/save.json' % (
        args.suite_id)
    case_dict = CASE_DICT[args.type]

    with open(args.csv_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            payload = {
                'app_id': APP_DICT[row['app']],
                'platform': row['platform'],
                'value_order': ORDER_DICT[row['wifi']]
            }

            for k, v in case_dict.items():
                payload['case_id'] = v
                payload['value'] = row[k]
                # print(json.dumps(payload, indent=1))

                r = requests.post(commit_url, data=payload)
                print(r.json())

            # print('------------')


if __name__ == '__main__':
    main()
