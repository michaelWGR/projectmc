# -*- coding:utf-8 -*-
import argparse
import csv
import os
import subprocess
import traceback
import re

time_format = "%b %d %Y %H:%M:%S"
header = ["No.", "Time", "Source", "Destination", "Protocol", "Length", "Info", "Src_port", "Dst_port"]
interface = "bridge100"


class Result:
    def __init__(self, **kwargs):
        key = kwargs.pop("key", None)

        # if len(key) != 2:
        #     raise Exception("Key:{} must be a set with 2 objects only.".format(key))

        self.num = kwargs.pop("num", None)
        self.key = key
        self.ip = kwargs.pop("ip", None)
        self.info = kwargs.pop("info", None)
        try:
            self.length = int(kwargs.pop("length", None))
        except:
            self.length = 0
        self.protocol = kwargs.pop("protocol", None)
        self.time = kwargs.pop("time", None)

    def __str__(self):
        return "key : {} , ip : {} , length : {} , protocol : {} , time : {}".format(
            self.key,
            self.ip,
            self.length,
            self.protocol,
            self.time)

    def get_seq(self):
        if "Seq" in self.info:
            m = re.search('Seq=\d+', self.info)
            result = m.group(0)
            return int(result[result.index("=") + 1:])
        else:
            return None

    class Row:
        def __init__(self, row):
            if not type(row) is dict:
                raise TypeError("{} must be a dict.".format(row))

            self.number = row["No."]
            self.time = row["Time"]
            self.source = row["Source"]
            self.destination = row["Destination"]
            self.protocol = row["Protocol"]
            self.length = row["Length"]
            self.info = row["Info"]
            self.src_port = row.pop("Src_port", None)
            self.dst_port = row.pop("Dst_port", None)


class Results:
    def __init__(self, result_instance):

        if not isinstance(result_instance, Result):
            raise TypeError("{} must be a Result object.".format(result_instance))

        self.results = [result_instance]
        self.key = result_instance.key
        self.count = 1
        self.ip = result_instance.ip
        self.length = {result_instance.length}
        self.total_length = result_instance.length
        self.protocol = result_instance.protocol
        self.b_time = result_instance.time
        self.e_time = result_instance.time

    def update(self, result_instance):

        if not isinstance(result_instance, Result):
            raise TypeError("{} must be a Result object.".format(result_instance))

        self.key = result_instance.key
        self.ip = result_instance.ip
        self.count += 1
        self.length.add(result_instance.length)
        self.total_length += result_instance.length
        self.protocol = result_instance.protocol
        self.e_time = result_instance.time

        self.results.append(result_instance)

    def get_seq_total(self):
        for result in self.results:
            pass

            # min_seq = self.results[0

    def __str__(self):
        return "key : {} , ip : {} , total_length : {} , count : {} ,length : {}, protocol : {} , b_time : {} , " \
               "e_time : {}".format(self.key, self.ip, self.total_length, self.count, self.length, self.protocol,
                                    self.b_time,
                                    self.e_time)

    def __eq__(self, other):
        if other.key == self.key:
            return True
        else:
            return False

    def get_package_rank(self):

        results_pkg_group_list = []

        for result in self.results:

            exist = False

            for results_pkg_group in results_pkg_group_list:

                if result.length in results_pkg_group.length:
                    exist = True
                    results_pkg_group.update(result)

            if not exist:
                new_packages = Results(result)
                results_pkg_group_list.append(new_packages)

        return sort_results(results_pkg_group_list)[:3]


def get_results(csv_file):
    results_list = []

    with open(csv_file) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:

            try:
                row_object = Result.Row(row)
                exist = False

                result = Result(key={"{}:{}".format(row_object.source, row_object.src_port),
                                     "{}:{}".format(row_object.destination, row_object.dst_port)},
                                ip={row_object.source, row_object.destination},
                                length=row_object.length,
                                protocol=row_object.protocol,
                                time=row_object.time,
                                info=row_object.info,
                                num=row_object.number)

                for results in results_list:
                    # and results.protocol == result.protocol
                    if results.key & result.key == results.key and results.ip & result.ip == results.ip:
                        results.update(result)
                        exist = True

                if not exist:
                    new_results = Results(result)
                    results_list.append(new_results)

            except Exception as e:
                traceback.print_exc()

    return results_list


def sort_results(results):
    if not type(results) is list:
        raise TypeError("Param {} must be a list".format(results))

    sorted_results = sorted(results, key=lambda x: x.total_length, reverse=True)
    return sorted_results


def clean_data(results_list):
    target = results_list[0]
    clean_results_list = []

    flag = 0

    for results in results_list:
        # and results.protocol == target.protocol
        if results.ip & target.ip == target.ip:
            clean_results_list.append(results)
            flag += results.total_length

    if len(clean_results_list) == 0:
        raise Exception("Clean results length is 0.")

    flag = flag / len(clean_results_list) / 3
    print "\nflag is {}".format(flag)
    i = 0

    for results in clean_results_list:
        if results.total_length > flag:
            i += 1

    return clean_results_list[:i]


def rank_results_packages(results_list):
    rank_results = []

    for results in results_list:
        packages_list = results.get_package_rank()

        rank_results.append(packages_list[0])

    return rank_results


def cal_results(results_list):
    # 1. 计算流量
    print ("\nCal:")
    min_b_time = min(float(results.b_time) for results in results_list)
    max_e_time = max(float(results.e_time) for results in results_list)
    total_length = sum(results.total_length for results in results_list)

    print ("min_begin_time : {} , max_e_time : {} , duration : {} , total_length : {:.2f} KB".format(min_b_time,
                                                                                                     max_e_time,
                                                                                                     max_e_time -
                                                                                                     min_b_time,
                                                                                                     total_length / 1024))
    print ("speed : {:.4f} KB/s".format(total_length / (max_e_time - min_b_time) / 1024))


def cal_seq(results_list):
    # 计算seq大小
    seq_list = []
    for results in results_list:
        last_seq = max(x.get_seq() for x in results.results)
        seq_list.append(last_seq)

    print ("\nCal Seq :")
    print ("seq list: {} ".format(seq_list))
    print ("sum is : {:.2f} KB ".format(sum(int(x) for x in seq_list) / 1024))


def stop_capture(capture_process):
    quit_command = raw_input("Press q and enter to quit the capture:")
    if quit_command.lower() == 'q':
        capture_process.terminate()
    else:
        stop_capture(capture_process)


def flush_data_to_csv(file_path):
    if not os.path.isfile(file_path):
        raise Exception("Can't find file {}".format(file_path))

    # time_epoch
    cmd = "tshark -r {} -T fields -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e _ws.col.Protocol " \
          "-e frame.len -e _ws.col.Info -e tcp.srcport -e udp.srcport -e tcp.dstport -e udp.dstport".format(
        file_path).split()
    output = subprocess.check_output(cmd)
    csv_file = "{}.csv".format(os.path.splitext(file_path)[0])

    with open(csv_file, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)

        for line in output.splitlines():
            csv_writer.writerow(re.split(r'\t+', line))

    return csv_file


def capture(file_path):
    # Check interface exist.
    output = subprocess.check_output("tcpdump -D".split())
    if interface not in output:
        raise Exception("{} is not in the interface list, pleace check your wifi sharing status.".format(interface))

    print ("Capturing...")
    cmd = "tcpdump -W 1 -w {} -t -i bridge100".format(file_path).split()
    p = subprocess.Popen(cmd)
    stop_capture(p)
    return file_path


def main():
    parser = argparse.ArgumentParser('Description')
    parser.add_argument('pcapng_file', help="pcap文件的绝对路径(e.g:/Users/tmp/test.pcapng)")
    args = parser.parse_args()
    pcapng_file = args.pcapng_file

    if not os.path.splitext(pcapng_file)[1] == ".pcapng":
        raise TypeError("Param {} must be a pcapng file.".format(pcapng_file))

    # Capture
    pcapng_file = capture(pcapng_file)

    # Get csv
    csv_file = flush_data_to_csv(pcapng_file)

    # Get results
    results_list = get_results(csv_file)
    sorted_results_list = sort_results(results_list)

    # Sort results
    max_length = 10
    index = len(sorted_results_list) if len(sorted_results_list) <= max_length else max_length

    print ("\nSorted results:")
    for i in range(0, index):
        print (sorted_results_list[i])

    # Clean results
    clean_results_list = clean_data(sorted_results_list)
    print ("\nClean results:")
    for clean_results in clean_results_list:
        print (clean_results)

    # Rank results by group by package
    # Return a list with all max length results
    rank_results_list = rank_results_packages(clean_results_list)
    print ("\nRank pkg results:")
    for rank_results in rank_results_list:
        print (rank_results)

    # Cal clean results
    cal_results(rank_results_list)

    # Cal seq
    cal_seq(clean_results_list)


if __name__ == '__main__':
    main()
