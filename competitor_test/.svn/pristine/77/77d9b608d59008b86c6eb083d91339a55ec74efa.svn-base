# -*- coding:utf-8 -*-

import argparse
import sys
import os
import csv
import subprocess
import numpy
import time,datetime


def find_trace_utility():
    pwd = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pwd, 'TraceUtility_gpu_8.3')


def parse_trace_cpu(trace_utility_path, trace_filepath, output_file):
    cmd = [trace_utility_path, trace_filepath]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    import time
    stdout, stderr = proc.communicate()
    timestamp_ = time.mktime(datetime.datetime.now().timetuple())
    with open(output_file, 'wb') as f:
        csv_writer = csv.writer(f)

        header = True
        cpus = []
        count = 0
        for line in stderr.splitlines():
            line_items = line.split(',')

            if header:
                if len(line_items) != 2 or all(
                                line_item not in ['Device Utilization', 'Tiler Utilization'] for line_item in
                                line_items):
                    # maybe some logs
                    continue
                header = False
                continue

            if not header and 0 != int(line_items[0]):
                cpus.append(float(line_items[0]))
            now_datetime_str = datetime.datetime.fromtimestamp(int(timestamp_) + count).strftime("%Y-%m-%d %H:%M:%S")
            csv_writer.writerow([now_datetime_str, int(timestamp_) + count, line_items[1],line_items[0]])
            header = False
            count += 1

        # avg_cpu = numpy.average(cpus)
        # stdev_cpu = numpy.std(cpus)
        # csv_writer.writerow(['-', '-', avg_cpu, stdev_cpu])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('trace_files', nargs='+')
    args = parser.parse_args()
    trace_utility_path = find_trace_utility()

    trace_files = args.trace_files
    for trace_file in trace_files:
        trace_file = os.path.abspath(trace_file)
        trace_filename = os.path.splitext(os.path.basename(trace_file))[0]
        trace_filedir = os.path.dirname(trace_file)
        (app, platform, case_name, time) = trace_filename.split('_')
        output_file = ''
        client = ''
        if case_name == 'actorperf':
            client = 'actor'
        else:
            client = 'viewer' 
        output_file = os.path.join(trace_filedir, '%s_%s_%s_%s.csv' % (app, platform, client + 'gpu', time))
        print output_file
        # output_file = os.path.join(trace_filedir, '%s_gpu.csv' % (trace_filename))
        parse_trace_cpu(trace_utility_path, trace_file, output_file)


if __name__ == "__main__":
    main()
