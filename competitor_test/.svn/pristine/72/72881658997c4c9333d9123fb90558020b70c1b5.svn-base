# -*- coding:utf-8 -*-

import os
import csv
import math

import argparse
import fnmatch
import itertools

import cv2
import numpy

__author__ = 'LibX'


def is_win():
    return os.name == 'nt'


def expand_wildcards(wildcards_path):
    dirpath = os.path.abspath(os.path.dirname(wildcards_path))
    wildcards_pattern = os.path.basename(wildcards_path)

    for filename in os.listdir(dirpath):
        if fnmatch.fnmatch(filename, wildcards_pattern):
            yield os.path.join(dirpath, filename)


def get_values(csv_reader, col, col_type=float):
    for row in csv_reader:
        if not row:
            # ignore empty line
            continue
        try:
            yield col_type(row[col])
        except ValueError:
            pass


class MinReducer(object):
    def __init__(self):
        self.min_val = None

    def reduce(self, value):
        if self.min_val is None or value < self.min_val:
            self.min_val = value

    def get_result(self):
        return self.min_val


class MaxReducer(object):
    def __init__(self):
        self.max_val = None

    def reduce(self, value):
        if self.max_val is None or value > self.max_val:
            self.max_val = value

    def get_result(self):
        return self.max_val


class AvgerageReducer(object):
    def __init__(self):
        self.value_sum = 0.0
        self.count = 0

    def reduce(self, value):
        self.value_sum += value
        self.count += 1

    def get_result(self):
        return self.value_sum / self.count


class StdDevReducer(object):
    def __init__(self):
        self.value_sq_sum = 0.0
        self.value_sum = 0.0
        self.count = 0

    def reduce(self, value):
        value_sq = float(value) * value

        self.value_sum += value
        self.value_sq_sum += value_sq
        self.count += 1

    def get_result(self):
        avg_val = self.value_sum / self.count
        return math.sqrt(self.value_sq_sum / self.count - avg_val * avg_val)


def get_reducer_by_type(calc_type):
    if calc_type == 'min':
        reducer = MinReducer()
    elif calc_type == 'max':
        reducer = MaxReducer()
    elif calc_type == 'avg':
        reducer = AvgerageReducer()
    elif calc_type == 'stddev':
        reducer = StdDevReducer()
    else:
        raise ValueError('invalid calc_type')

    return reducer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--calc-type', action='append', dest='calc_types')
    parser.add_argument('col', type=int)
    parser.add_argument('csv_paths', nargs='+')
    args = parser.parse_args()

    if is_win():
        csv_paths = itertools.chain(*[expand_wildcards(csv_path) for csv_path in args.csv_paths])
    else:
        csv_paths = args.csv_paths

    col = int(args.col)
    for csv_path in csv_paths:
        reducers = [get_reducer_by_type(calc_type) for calc_type in args.calc_types]

        csv_path = os.path.abspath(csv_path)
        with open(csv_path, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            values = get_values(csv_reader, col)

            for value in values:
                for reducer in reducers:
                    reducer.reduce(value)

            calc_values = [str(reducer.get_result()) for reducer in reducers]

        print '%s,%s' % (os.path.basename(csv_path), ','.join(calc_values))


if __name__ == '__main__':
    main()
