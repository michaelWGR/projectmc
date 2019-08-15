# -*- coding:utf-8 -*-

import argparse
import sys
import os
import csv
import numpy as np


def CalMos(txt_paths, output_base):

    if output_base is None:
        dest_path = os.path.realpath(os.path.join(
            os.path.dirname(str(txt_paths[0])), 'mos_result.csv'))
    else:
        dest_path = os.path.abspath(output_base)

    # 生成csv文件
    with open(dest_path, 'wb+') as csv_wf:
        csv_writer = csv.writer(csv_wf)
        csv_writer.writerow(['app', 'platform', 'wifi', '3_4_max', '3_4_min',
                             '3_4_avg', '3_4_std', '4_3_max', '4_3_min', '4_3_avg', '4_3_std'])

        # 遍历每个txt文件
        for txt_path in txt_paths:
            txt_path = os.path.abspath(txt_path)
            txt_file = os.path.basename(txt_path)
            if txt_file.endswith('report.txt') and ('mos' in txt_file):
                # print txt_file
                txt_file_split = txt_file.split('_')
                app = txt_file_split[0]
                platform = txt_file_split[1]
                wifi = txt_file_split[3]

                mos_data = {
                    '3_4': [],
                    '4_3': [],
                    'max3_4': 0,
                    'min3_4': 0,
                    'avg3_4': 0,
                    'std3_4': 0,
                    'max4_3': 0,
                    'min4_3': 0,
                    'avg4_3': 0,
                    'std4_3': 0
                }

                with open(txt_path, 'r') as txt_rf:
                    for line in txt_rf:
                        if 'P863_SUMMARY_RESULT' in line:
                            arr_line = line.split(',')
                            chan_dw = str(int(arr_line[0]) + 1)
                            if chan_dw == '3':
                                chan = '4_3'
                            elif chan_dw == '4':
                                chan = '3_4'
                            # 获取mos数据
                            try:
                                mos_data[chan].append(float(arr_line[10]))
                            except Exception:
                                print '{}: mos data is not digital'.format(txt_file)
                                break

                    if mos_data['3_4']:
                        mos_data['max3_4'] = max(mos_data['3_4'])
                        mos_data['min3_4'] = min(mos_data['3_4'])
                        mos_data['avg3_4'] = np.mean(mos_data['3_4'])
                        mos_data['std3_4'] = np.std(mos_data['3_4'], ddof=1)
                        mos_data['max4_3'] = max(mos_data['4_3'])
                        mos_data['min4_3'] = min(mos_data['4_3'])
                        mos_data['avg4_3'] = np.mean(mos_data['4_3'])
                        mos_data['std4_3'] = np.std(mos_data['4_3'], ddof=1)
                        csv_writer.writerow([app, platform, wifi, mos_data['max3_4'], mos_data['min3_4'], mos_data['avg3_4'], mos_data[
                                            'std3_4'], mos_data['max4_3'], mos_data['min4_3'], mos_data['avg4_3'], mos_data['std4_3']])
                    else:
                        print '{}: mos data is null'.format(txt_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('txt_paths', help='file path', nargs='+')
    parser.add_argument('-ob', '--output-base', help='output base dir')
    args = parser.parse_args()

    # 统计MOS值
    CalMos(args.txt_paths, args.output_base)


if __name__ == '__main__':
    main()
