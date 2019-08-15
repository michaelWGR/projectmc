# -*- coding:utf-8 -*-
import argparse
import csv


def main():
    parser = argparse.ArgumentParser('Description')
    parser.add_argument('file_path', help='文件的位置')
    args = parser.parse_args()
    file_path = args.file_path
    cal_results(get_result_from_csv(file_path))


def get_result_from_csv(args_file_path):
    """
    Get data structure from csv.
    :param args_file_path:
    :return:
    """
    results = {}
    with open(args_file_path) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            # key = get_key_from_info(row['Source'], row['Destination'], row['Info'], row['Protocol'])
            key = "{}:{}_{}:{}_{}".format(row['Source'], row['Src_port'], row['Destination'], row['Dst_port'],
                                          row['Protocol'])
            key_reverse = "{}:{}_{}:{}_{}".format(row['Destination'], row['Dst_port'], row['Source'], row['Src_port'],
                                                  row['Protocol'])
            if key is None:
                continue
            if key not in results and key_reverse not in results:
                # 如果发现结果集里面没有这个 key : s -> d 或者 key : d -> s 对应的值，那么初始化它
                results[key] = {
                    'time_begin': row['Time'], 'time_end': row['Time'], 'lengths': [row['Length']]
                }
            elif key in results:
                # 如果结果集里面已经有 key : s -> d 了，那么就更新这个结果集
                results[key]['time_end'] = row['Time']
                results[key]['lengths'].append(row['Length'])
            elif key_reverse in results:
                # 如果结果集里面已经有 key : s -> d  了，那么就更新这个结果集
                results[key_reverse]['time_end'] = row['Time']
                results[key_reverse]['lengths'].append(row['Length'])

    return results


def cal_results(args_results):
    sorted_results = sorted(args_results.items(), key=lambda x: len(x[1]['lengths']), reverse=True)
    print("\nindex c_port              <-> s_port               protocol nums")
    # 输出最多前3的结果集，确认一下正确性
    for i in range(0, 3):
        if i < len(sorted_results):
            key_items = sorted_results[i][0].split('_')
            print("{}     {}  <-> {}   {}      {}".format(i + 1, key_items[1], key_items[0], key_items[2],
                                                          len(sorted_results[i][1]['lengths'])))

    print("\nChoose {} <-> {} to cal.".format(sorted_results[0][0].split('_')[1], sorted_results[0][0].split('_')[0]))
    result_dict = sorted_results[0][1]
    time_begin = float(result_dict['time_begin'])
    time_end = float(result_dict['time_end'])
    duration = time_end - time_begin
    length_total = 0
    for length in result_dict['lengths']:
        length_total += int(length)
    counts = len(result_dict['lengths'])
    kbs = length_total / duration / 1024
    print("{} <-> {} length_total : {:.2f}kB ({:.2f}MB) duration : {:.4f}, counts : {}, kB/s : {:.4f}\n".format(
        sorted_results[0][0].split('_')[1], sorted_results[0][0].split('_')[0],
        length_total / 1024.00, length_total / 1024.00 / 1024.00, duration, counts,
        kbs))


if __name__ == '__main__':
    main()
