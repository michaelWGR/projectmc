# -*- coding:utf-8 -*-

import argparse
import sys
import os
import csv
import numpy as np


def CalDelay(txt_paths, output_base):

    if output_base is None:
        dest_path = os.path.realpath(os.path.join(
            os.path.dirname(str(txt_paths[0])), 'delay_result.csv'))
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
            if txt_file.endswith('report.txt') and ('delay' in txt_file):
                txt_file_split = txt_file.split('_')
                app = txt_file_split[0]
                platform = txt_file_split[1]
                wifi = txt_file_split[3]

                delay_data = {
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
                tag = 0 #标志该段数据是否有效

                with open(txt_path, 'r') as txt_rf:
                    for line in txt_rf:
                        if ('DELAY_CYCLE_STATS' in line) and ('SUCCESS' in line):
                            tag = 1
                            line_split = line.split(',')
                            voice1 = line_split[17]
                            voice2 = line_split[19]
                            chan_up = str(int(line_split[16]) + 1)
                            chan_dw = str(int(line_split[18]) + 1)
                            chan = chan_up + '_' + chan_dw
                            if voice1 != '165' or voice2 != '200':
                                print 'voice1 = {}, voice2 = {}'.format(voice1, voice2)
                                break

                        if tag == 1 and 'DELAY_RESULT' in line:
                            arr_line = line.split(',')
                            # 获取delay数据
                            try:
                                delay_data[chan].append(float(arr_line[9]))
                            except Exception:
                                print '{}: delay data is not digital'.format(txt_file)
                                break

                    if delay_data['3_4']:
                        delay_data['max3_4'] = max(delay_data['3_4'])
                        delay_data['min3_4'] = min(delay_data['3_4'])
                        delay_data['avg3_4'] = np.mean(delay_data['3_4'])
                        delay_data['std3_4'] = np.std(delay_data['3_4'], ddof=1)
                        delay_data['max4_3'] = max(delay_data['4_3'])
                        delay_data['min4_3'] = min(delay_data['4_3'])
                        delay_data['avg4_3'] = np.mean(delay_data['4_3'])
                        delay_data['std4_3'] = np.std(delay_data['4_3'], ddof=1)
                        csv_writer.writerow([app, platform, wifi, delay_data['max3_4'], delay_data['min3_4'], delay_data['avg3_4'], delay_data[
                            'std3_4'], delay_data['max4_3'], delay_data['min4_3'], delay_data['avg4_3'], delay_data['std4_3']])
                    else:
                        print '{}: delay data is null'.format(txt_file)





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('txt_paths', nargs='+', help='input base dir')
    parser.add_argument('-ob', '--output-base', help='output base dir')
    args = parser.parse_args()

    # 统计delay值
    CalDelay(args.txt_paths, args.output_base)


if __name__ == '__main__':
    main()
