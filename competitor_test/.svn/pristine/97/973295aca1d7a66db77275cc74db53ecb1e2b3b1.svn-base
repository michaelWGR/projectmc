# -*- coding:utf-8 -*-

import argparse
import sqlite3
import sys
import os
import csv
import time
import datetime

def parse_sqlite_file(sqlite_filepath, output_file):
    
    connection = sqlite3.connect(sqlite_filepath)
    cursor = connection.cursor()

    datas = []

    total_rx_bytes = 0
    total_tx_bytes = 0
    total_time = 0

    sql = 'select sum(rxBytes),sum(txBytes),intervalNumber from interval group by intervalNumber order by intervalNumber'
    cursor.execute(sql)

    rows = cursor.fetchall()
    re_sum = 0
    send_sum = 0
    timestamp_ = time.mktime(datetime.datetime.now().timetuple())
    for row in rows:
        if row[2] == -1:
            continue
        re_sum += int(row[0])
        send_sum += int(row[1])
        second_ = int(timestamp_) + int(row[2])
        now_datetime_str = datetime.datetime.fromtimestamp(second_).strftime("%Y-%m-%d %H:%M:%S")
        datas.append({'rx_bytes':re_sum,'tx_bytes':send_sum,'time': now_datetime_str, 'second': second_})

    # total_rx_bytes = sum([data['rx_bytes'] for data in datas])
    # total_tx_bytes = sum([data['tx_bytes'] for data in datas])
    # total_time = max([data['time'] for data in datas])
    
    with open(output_file,'wb') as write_file:
        csv_writer = csv.writer(write_file)
        #csv_writer.writerow(['time','rx_bytes','tx_bytes'])
        for data in datas: 
            csv_writer.writerow([data['time'],data['second'], data['rx_bytes'],data['tx_bytes']])

        # csv_writer.writerow(["-",str(total_rx_bytes/1024./1024.),str(total_tx_bytes/1024./1024.)])
        # csv_writer.writerow(["-",str(total_rx_bytes/1024./total_time),str(total_tx_bytes/1024./total_time)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('trace_files', nargs='+')
    args = parser.parse_args()

    trace_files = args.trace_files
    for trace_file in trace_files:
        trace_file = os.path.abspath(trace_file)
        trace_filename = os.path.splitext(os.path.basename(trace_file))[0]
        trace_filedir = os.path.dirname(trace_file)

        for parent_dir, dir_names, filenames in os.walk(trace_file):
            for filename in filenames:
                if not os.path.splitext(filename)[1] == '.netconndb':
                    continue
                try:
                    sqlite_filepath = os.path.join(parent_dir, filename)
                    (app, platform, case_name, time) = trace_filename.split('_')
                    output_file = ''
                    client = ''
                    if case_name == 'actorperf':
                        client = 'actor'
                    else:
                        client = 'viewer'
                    run_name = os.path.splitext(os.path.basename(os.path.dirname(sqlite_filepath)))[0]
                    output_file = os.path.join(trace_filedir, '%s_%s_%s_%s_%s.csv' % (app, platform, client + 'network', run_name, time))
                    # output_file = os.path.join(trace_filedir, '%s_%s_network.csv' % (trace_filename, run_name))
                    
                    parse_sqlite_file(sqlite_filepath, output_file)
                except Exception, e:
                    print 'parse ' + run_name + ' error'


if __name__ == "__main__":
    main()