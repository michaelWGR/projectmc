# -*- coding:UTF-8 -*-

from __future__ import print_function

import os
import sys
import math
import csv
import argparse


START_NUM = 302
END_NUM = 7501
SRC_FRAME_RATE = 60.0
TARGET_FRAME_RATE = 30.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-s', '--start-num', default=START_NUM, type=int, help='start num')
    parser.add_argument('-e', '--end-num', default=END_NUM, type=int, help='end num')
    parser.add_argument('-sr', '--src-frame-rate', default=SRC_FRAME_RATE, type=float, help='src frame rate')
    parser.add_argument('-tr', '--target-frame-rate', default=TARGET_FRAME_RATE, type=float, help='target frame rate')
    parser.add_argument('csvs_or_dirs', nargs='+')
    args = parser.parse_args()

    start_num, end_num, src_frame_rate, target_frame_rate = args.start_num, args.end_num, args.src_frame_rate, args.target_frame_rate

    target_csv_paths = args.csvs_or_dirs

    for target_csv_path in target_csv_paths:
        print('input', target_csv_path)
        target_csv_dir = os.path.dirname(target_csv_path)
        target_csv_name = os.path.splitext(os.path.basename(target_csv_path))[0]
        if target_csv_name.endswith('_number'):
            target_csv_name = target_csv_name[:-len('_number')]
        result_csv_path = os.path.join(target_csv_dir, target_csv_name + '_result.csv')

        frame_lists = {}
        percent_list = []

        with open(target_csv_path, 'rb') as target_csv_file:
            target_csv = csv.reader(target_csv_file)
            for row in target_csv:
                num = row[1]
                if ' ' in row[1]:
                    num = num.replace(' ', '')

                try:
                    num = int(num)
                except ValueError:
                    print('can not parse to int %s,%s' % (row[0],row[1]))

                if num < start_num or num > end_num:
                    continue

                second = int(math.floor((num - start_num) / src_frame_rate)) + 1
                if second not in frame_lists:
                    frame_lists[second] = []

                frame_list = frame_lists[second]
                frame_list.append(num)

        print('output', result_csv_path)
        with open(result_csv_path, 'wb') as result_csv_file:
            result_csv = csv.writer(result_csv_file)
            result_csv.writerow(['second', 'frame_count', 'frame_percent'])
            
            last_second = int(math.floor((end_num - start_num) / src_frame_rate)) + 1
            for second in range(1, last_second + 1):
                frame_list = frame_lists.get(second, [])
                valid_count = len(set(frame_list))
                percent = valid_count / target_frame_rate
                percent_list.append(percent)
                result_csv.writerow([second, valid_count, valid_count / target_frame_rate])
            avg_percent = sum(percent_list)/len(percent_list)
            result_csv.writerow(['-', '-', avg_percent])

if __name__ == "__main__":
    main()

