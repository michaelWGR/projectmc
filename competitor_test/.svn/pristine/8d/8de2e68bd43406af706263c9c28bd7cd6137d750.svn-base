# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import csv
import hashlib
import argparse
import tempfile
import datetime
import functools
import subprocess

import cv2
import numpy


def _find_bin_by_path(path, exe):
    exe_path = os.path.join(path, exe)
    if os.path.exists(exe_path) and os.path.isfile(exe_path):
        return exe_path
    exe_path = os.path.join(path, '%s.exe' % (exe,))
    if os.path.exists(exe_path) and os.path.isfile(exe_path):
        return exe_path


def find_bin(bin_name, environs=None):
    bin_path = None

    environs = environs if environs is not None else []
    environs += ['PATH']

    for environ in environs:
        environ_paths = os.environ.get(environ, None)
        if environ_paths is None:
            continue

        paths = environ_paths.split(os.pathsep)
        for path in paths:
            bin_path = _find_bin_by_path(path, bin_name)
            if bin_path is not None:
                return bin_path

            # try ${path}/bin
            bin_path = _find_bin_by_path(os.path.join(path, 'bin'), bin_name)
            if bin_path is not None:
                return bin_path

    return None


@functools.total_ordering
class Version(object):
    def __init__(self, full):
        self.full, version_str = full, full

        self.suffix = ''
        for i in range(len(version_str)):
            if not str.isdigit(version_str[i]) and '.' != version_str[i]:
                self.suffix = version_str[i:]
                version_str = version_str[:i]
                break

        version_splits = version_str.split('.')

        self.major = int(version_splits[0]) if version_splits else 0
        self.minor = int(version_splits[1]) if version_splits and len(version_splits) > 1 else 0
        self.rev = int(version_splits[2]) if version_splits and len(version_splits) > 2 else 0

    def __eq__(self, other):
        return ((self.major, self.minor, self.rev, self.suffix) == (other.major, other.minor, other.rev, other.suffix))

    def __lt__(self, other):
        return ((self.major, self.minor, self.rev, self.suffix) < (other.major, other.minor, other.rev, other.suffix))


class Tesseract(object):
    min_can_use_std_version = Version('3.03')

    class _TempSession(object):
        def __init__(self):
            self.tempfile_fd, self.tempfile_path = None, None

        def open(self):
            self.tempfile_fd, self.tempfile_path = tempfile.mkstemp(prefix='number_detector_', suffix='.txt')

        def close(self):
            if self.tempfile_fd is not None:
                os.close(self.tempfile_fd)

            if self.tempfile_path is not None:
                os.remove(self.tempfile_path)

            self.tempfile_fd = None
            self.tempfile_path = None


        def __enter__(self):
            self.open()
            return None

        def __exit__(self, type, value, tb):
            return self.close()

    def __init__(self, tesseract_path=None):
        self.tesseract_path = self.find_bin() if tesseract_path is None else tesseract_path
        self.version = self._get_version(self.tesseract_path)

        self.temp_session = None

    @classmethod
    def find_bin(cls):
        return find_bin('tesseract', environs=['TESSERACT_HOME'])

    @classmethod
    def _get_version(cls, tesseract_path):
        cmd = [tesseract_path, '-v']

        child = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        _, stderr = child.communicate()
        lines = stderr.splitlines()
        version_line = lines[0] if lines else ''
        assert version_line.startswith('tesseract')

        version_str = version_line[len('tesseract') + 1:]
        return Version(version_str)

    def temp(self):
        self.temp_session = self._TempSession()
        return self.temp_session

    def can_use_std(self):
        self.version >= self.min_can_use_std_version

    def parse_by_file(self, filepath):
        has_session = self.temp_session is not None
        temp_session = self.temp_session if has_session else self._TempSession()

        try:
            if not has_session:
                temp_session.open()

            cmd = [self.tesseract_path, filepath, os.path.splitext(temp_session.tempfile_path)[0], '-psm', '7']

            child = subprocess.Popen(cmd)
            stdout, stderr = child.communicate()
            child.poll()

            with open(temp_session.tempfile_path, 'rb') as tmp_file:
                line = next(tmp_file, None)
            line = line.splitlines()[0] if line else ''
            return line
        finally:
            if not has_session:
                temp_session.close()

    def parse_by_stdin(self, image):
        raise NotImplementedError()


def find_ffmpeg():
    return find_bin('ffmpeg', environs=['FFMPEG_HOME'])


def get_frame_dir(video_path, output_base_dir=None):
    video_path = os.path.abspath(video_path)
    video_file_name = os.path.basename(video_path)
    video_name = os.path.splitext(video_file_name)[0]
    video_parent_dir = os.path.dirname(video_path)

    output_base_dir = video_parent_dir if output_base_dir is None else output_base_dir
    return os.path.join(output_base_dir, video_name)


def extract_frames(video_path, frame_rate, output_base_dir=None, frame_type='bmp'):
    video_path = os.path.abspath(video_path)
    video_file_name = os.path.basename(video_path)
    video_name = os.path.splitext(video_file_name)[0]

    frame_dir = get_frame_dir(video_path, output_base_dir=output_base_dir)

    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)

    frame_pattern = os.path.join(frame_dir, video_name + '%5d.' + frame_type)

    ffmpeg_path = find_ffmpeg()
    assert ffmpeg_path is not None

    cmd = [ffmpeg_path, '-i', video_path, '-r', str(frame_rate), '-f', 'image2', frame_pattern]
    child = subprocess.Popen(cmd, cwd=os.path.dirname(ffmpeg_path))
    child.wait()

    return frame_dir


def get_frame_filepaths(frame_dir, frame_type='bmp'):
    frame_ext = '.' + frame_type
    frame_filepaths = [os.path.join(frame_dir, _) for _ in os.listdir(frame_dir) if os.path.isfile(os.path.join(frame_dir, _)) and os.path.splitext(_)[1].lower() == frame_ext]
    return frame_filepaths


def duplication(frame_dir, frame_type='bmp'):
    frame_filepaths = get_frame_filepaths(frame_dir, frame_type=frame_type)

    frames_md5 = {}
    for frame_filepath in frame_filepaths:
        md5obj = hashlib.md5()
        with file(frame_filepath, 'rb') as frame_file:
            md5obj.update(frame_file.read())
        md5 = md5obj.hexdigest()
        if md5 not in frames_md5:
            frames_md5[md5] = frame_filepath
        else:
            os.remove(frame_filepath)
    return frames_md5.values()


def get_roi_frame(frame, roi_type):
    shape = frame.shape
    assert shape[0] in (459, 918) or shape[0] in (750,1334)

    assert roi_type in ('android', 'ios', 'ios_mov')
    if roi_type == 'android':
        if shape[0] == 720:
            x = 606
            y = 327
            width = 140
            height = 67
            # img = img[327:327+67, 606:606+140]
        elif shape[0] == 1080:
            x = 910
            y = 490
            width = 206 - 6
            height = 101 - 9
            # img = img[490:490+101, 910:910+206]
    elif roi_type == 'ios':
        if shape[0] == 918:
            x = 910 + 4
            y = 327 + 4
            width = 205
            height = 105 - 9 - 4
            # # img = img[327:327+67, 606:606+140]
        elif shape[0] == 459:
            x = 454 + 4
            y = 162 + 4
            width = 103
            height = 59 - 9 - 4
            # img = img[490:490+101, 910:910+206]
    elif roi_type == 'ios_mov':
        if shape[0] == 750:
            x = 633
            y = 342
            width = 139
            height = 69
        elif shape[0] == 1080:
            x = 910
            y = 490
            width = 201
            height = 101
        else:
            assert False

    roi_frame = frame[y:y+height, x:x+width]
    roi_frame = cv2.GaussianBlur(roi_frame, (3,3), 1.5)

    retval, roi_frame = cv2.threshold(roi_frame, 200, 255, cv2.THRESH_BINARY)
    return roi_frame


def get_roi_frame_dir(frame_dir, output_base_dir=None):
    frame_dir = os.path.abspath(frame_dir)
    video_name = os.path.basename(frame_dir)
    video_parent_dir = os.path.dirname(frame_dir)
    output_base_dir = video_parent_dir if output_base_dir is None else output_base_dir

    return os.path.join(output_base_dir, video_name + '_roi')


def write_roi_frame(frame_dir, roi_type, output_base_dir=None, frame_type='bmp'):
    roi_frame_dir = get_roi_frame_dir(frame_dir, output_base_dir=output_base_dir)
    if not os.path.exists(roi_frame_dir):
        os.makedirs(roi_frame_dir)

    roi_frame_filepaths = []

    frame_filepaths = get_frame_filepaths(frame_dir, frame_type=frame_type)
    for frame_filepath in frame_filepaths:
        frame = cv2.imread(frame_filepath, cv2.IMREAD_GRAYSCALE)
        roi_frame = get_roi_frame(frame, roi_type)

        roi_frame_filepath = os.path.join(roi_frame_dir, os.path.basename(frame_filepath))

        cv2.imwrite(roi_frame_filepath, roi_frame)
        roi_frame_filepaths.append(roi_frame_filepath)

    return roi_frame_dir, roi_frame_filepaths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--roi-type', type=str, default='android', help='roi type')
    parser.add_argument('--just-extract', action='store_true', default=False, help='just extract frames')
    parser.add_argument('--just-roi', action='store_true', default=False, help='just roi frames')
    parser.add_argument('--just-detect', action='store_true', default=False, help='just detect frames')
    parser.add_argument('-ob', '--output-base', help='output base dir') 
    parser.add_argument('videos_or_frame_dirs', nargs='+') #需要输入两个路径：原始帧路径和失真帧路径。原始帧路径放前面 失真帧路径放后面
    args = parser.parse_args()

    tesseract = Tesseract()

    #frame_rate = args.frame_rate
    distinct = True  # args.distinct
    frame_type = 'bmp'
    roi_type = args.roi_type
    output_base = args.output_base

    just_flags = (just_extract, just_roi, just_detect,) = (args.just_extract, args.just_roi, args.just_detect,)
    assert sum( 1 for _ in just_flags if _ ) <= 1

    all_do = not any(just_flags)
    do_flags = [_ or all_do for _ in just_flags]

    do_extract, do_roi, do_detect = do_flags

    if len(args.videos_or_frame_dirs)!=2:
        print "please input two dirs: source frames dir and stream frames dir"
        raise IOError
    for video_or_frame_dir in args.videos_or_frame_dirs:
        starttime = datetime.datetime.now()
        assert not video_or_frame_dir.endswith(os.pathsep)

        video_or_frame_dir = os.path.abspath(video_or_frame_dir)
        print('detection start %s' % (video_or_frame_dir, ))
        output_base_dir = os.path.dirname(video_or_frame_dir) if output_base is None else output_base

        frame_dir = get_frame_dir(video_or_frame_dir, output_base_dir=output_base_dir)

        #output_csv_path = os.path.join(output_base_dir, video_name + '_number.csv')

        print('roi from %s' % (frame_dir, ))
        roi_frame_dir, roi_frame_filepaths = write_roi_frame(frame_dir, roi_type, output_base_dir=output_base_dir, frame_type=frame_type)

        #print('tesseract %s to %s' % (roi_frame_dir, output_csv_path))

        # 原始帧中的数字识别，保存成一个字典，key为数字，value为帧图片路径
        if args.videos_or_frame_dirs.index(video_or_frame_dir) == 0:
            srcSources = {}
            for roi_frame_filepath in roi_frame_filepaths:
                tesseract_result = tesseract.parse_by_file(roi_frame_filepath)
                tesseract_result = tesseract_result.strip()
                frame_name = os.path.abspath(roi_frame_filepath)
                if tesseract_result.isdigit():
                    if tesseract_result in srcSources.keys():
                        srcSources[tesseract_result].append(frame_name)
                    else:
                        srcSources[tesseract_result] = []
                        srcSources[tesseract_result].append(frame_name)
                else:
                    continue

        # 失真帧中的数字识别，每次识别都会寻找原始帧中数字与之对应的图片，然后写入csv
        else:
            with open(video_or_frame_dir +'.csv', 'wb') as csvfile:
                writer = csv.writer(csvfile)
                for roi_frame_filepath in roi_frame_filepaths:
                    tesseract_result = tesseract.parse_by_file(roi_frame_filepath)
                    tesseract_result = tesseract_result.strip()
                    frame_name = os.path.abspath(roi_frame_filepath) 
                    if tesseract_result.isdigit():
                        if tesseract_result in srcSources.keys():
                            for srcframe in srcSources[tesseract_result]:
                                writerow = (frame_name, srcframe, tesseract_result)
                                writer.writerow(writerow)
                    else:
                        continue  

        endtime = datetime.datetime.now()

        # print run time
        timedelta = endtime - starttime
        run_time_splits = str(timedelta).split(':')
        run_time_str = '%s hours %s minutes %s seconds' % (run_time_splits[0], run_time_splits[1], run_time_splits[2])
        print('total use %d microseconds (%s)' % ((endtime - starttime).microseconds, run_time_str))


if __name__ == '__main__':
    main()