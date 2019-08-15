# -*- coding:utf-8 -*-

import argparse
import sys
import os
import csv
import subprocess
import numpy
import datetime

APP_PROCESS_NAME = {
    'yy': {'actor': 'YYMobile', 'viewer': 'YYMobile'},
    'hy': {'actor': 'live', 'viewer': 'kiwi'},
    'mo': {'actor': 'MomoChat', 'viewer': 'MomoChat'},
    'yk': {'actor': 'inke', 'viewer': 'inke'},
    'bg': {'actor': 'bigoshow', 'viewer': 'bigoshow'},
    'xm': {'actor': 'VansLive', 'viewer': 'VansLive'},
    'lm': {'actor': 'KEWL', 'viewer': 'KEWL'},
    'pd': {'actor': '', 'viewer': 'PandaTV-ios'},
    'dy': {'actor': '', 'viewer': 'DYZB'},
    'dyassist': {'actor': 'LiveAssist', 'viewer': 'DYZB'},
    'csassist': {'actor': 'ChushouRec', 'viewer': 'chushoutv-pro'},
    'yyassist': {'actor': 'yyassist4game', 'viewer': 'YYMobile'},
    'hyassist': {'actor': 'live', 'viewer': 'kiwi'},
}

def find_trace_utility():
    pwd = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pwd, 'TraceUtility_cpu_8.3')


def get_process_name(arg_app_name, arg_client):
    return APP_PROCESS_NAME.get(arg_app_name, {}).get(arg_client, None)
    

def parse_trace_cpu(trace_utility_path, trace_filepath, proc_name, output_file):
    cmd = [trace_utility_path, trace_filepath, proc_name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    import time
    timestamp_ = time.mktime(datetime.datetime.now().timetuple())
    with open(output_file, 'wb') as f:
        csv_writer = csv.writer(f)

        header = True
        cpus = []

        for line in stderr.splitlines():
            line_items = line.split(',')

            if header:
                if len(line_items) != 3 or all(line_item not in ['SampleNumber', 'Command', 'CPUUsage'] for line_item in line_items):
                    # maybe some logs
                    continue
                header = False
                continue

            try:
                sample_number = int(line_items[0])
            except ValueError:
                continue

            if 0 != sample_number:
                cpus.append(float(line_items[2]))
            
            now_datetime_str = datetime.datetime.fromtimestamp(int(timestamp_) + int(line_items[0])).strftime("%Y-%m-%d %H:%M:%S")

            csv_writer.writerow([now_datetime_str, line_items[2]])
            header = False

        # avg_cpu = numpy.average(cpus)
        # stdev_cpu = numpy.std(cpus)
        # csv_writer.writerow(['-','-',avg_cpu,stdev_cpu])


class DefaultOutputFile(object):
    def __init__(trace_filename, proc_name):
        self.trace_filename = trace_filename
        self.proc_name = proc_name

    def get_filename(self, target_proc_name):
        if target_proc_name == self.proc_name:
            output_filename = '%s_%s_%s.csv' % (self.trace_filename, 'cpu', time)
        elif proc_name == 'mediaserverd':
            output_filename = '%s_%s_%s.csv' % (self.trace_filename, 'mediaservercpu', time)
        else:
            raise ValueError('%s  is not supported' % (target_proc_name,))

        return output_filename


class ConfiguredOutputFile(object):
    def __init__(self, app, platform, client, proc_name, time):
        self.app, self.platform, self.client, self.time = app, platform, client, time
        self.proc_name = proc_name

    def get_filename(self, target_proc_name):
        if target_proc_name == self.proc_name:
            output_filename = '%s_%s_%s_%s.csv' % (self.app, self.platform, self.client + 'cpu', self. time)
        elif target_proc_name == 'mediaserverd':
            output_filename = '%s_%s_%s_%s.csv' % (self.app, self.platform, self.client + 'mediaservercpu', self.time)
        else:
            raise ValueError('%s  is not supported' % (target_proc_name,))

        return output_filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('--proc-name', default=None)
    parser.add_argument('trace_files', nargs='+')
    args = parser.parse_args()

    proc_name = args.proc_name
    trace_utility_path = find_trace_utility()

    trace_files = args.trace_files
    for trace_file in trace_files:
        trace_file = os.path.abspath(trace_file)
        trace_filename = os.path.splitext(os.path.basename(trace_file))[0]
        trace_filedir = os.path.dirname(trace_file)

        if proc_name:
            output_file = DefaultOutputFile(trace_filename, proc_name)
        else:
            (app, platform, case_name, time) = trace_filename.split('_')
            client = ''
            if case_name == 'actorperf':
                client = 'actor'
            elif case_name == 'viewerperf':
                client = 'viewer'
            else:
                # TODO warning
                print 'case name %s is not supported' % (case_name, )
                continue

            proc_name = get_process_name(app, client)
            if not proc_name:
                # TODO warning
                print 'can not get process name by app=%s, client=%s' % (app, client)

            output_file = ConfiguredOutputFile(app, platform, client, proc_name, time)

        for cpu_proc_name in (proc_name, 'mediaserverd'):
            print 'parsing %s %s' % (trace_file, cpu_proc_name)

            output_filepath = os.path.join(trace_filedir, output_file.get_filename(cpu_proc_name))

            parse_trace_cpu(trace_utility_path, trace_file, cpu_proc_name, output_filepath)


if __name__ == "__main__":
    main()
