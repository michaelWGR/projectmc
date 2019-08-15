# -*-coding:utf-8-*-

import os
import sys
import csv
import subprocess
import argparse

import cv2
import numpy

from matplotlib import pyplot as plt


def timedelta_milliseconds(timedelta):
    return (timedelta.microseconds + (timedelta.seconds + timedelta.days * 24 * 3600) * 10**6) / 10**3


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


def find_ffmpeg():
    return find_bin('ffmpeg', environs=['FFMPEG_HOME'])


def get_video_shape(video_path):
    import json

    ffprobe_path = find_bin('ffprobe')

    cmd = [ffprobe_path,
           '-v', 'error',
           '-show_entries', 'stream=width,height:stream_tags=rotate',
           '-of', 'json',
           video_path]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = child.communicate()

    video_info = json.loads(stdout)
    stream_infos = video_info.get('streams', None)
    if stream_infos is None:
        return None

    # find first stream which contains 'width' and 'height'
    stream_info = next(
        (_ for _ in video_info['streams'] if 'width' in _ and 'height' in _), None)
    if stream_info is None:
        return None

    size = [stream_info['width'], stream_info['height']]
    tags = stream_info.get('tags', None)
    rotate = int(tags.get('rotate', 0)) if tags is not None else 0
    if rotate == 90 or rotate == 270:
        size.reverse()
    return tuple(size)


class VideoFrames(object):
    def __init__(self, video_path, frame_rate=None, video_shape=None, buffer_size=None):
        super(VideoFrames, self).__init__()
        self.video_path = os.path.abspath(video_path)
        self.video_shape = video_shape if video_shape is not None else get_video_shape(self.video_path)
        self.frame_rate = frame_rate

        self.frame_size = self.video_shape[0] * self.video_shape[1] * 3

        self.ffmpeg_path = find_bin('ffmpeg')
        self.ffmpeg_proc = None
        self.buffer_size = buffer_size if buffer_size is not None else self.frame_size * 10

        self._state = 1  # 1==ready, 2==running, 3==finished
        self._current_frame_num = 0
        self._current_frame = None

    def __enter__(self):
        self.setUp()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tearDown()

    def __iter__(self):
        while True:
            frame_num, frame = self.next()
            yield frame_num, frame

    def setUp(self):
        if self._state != 1:
            raise ValueError()

        cmd = [self.ffmpeg_path,
               '-i', self.video_path,
               '-f', 'image2pipe',
               '-pix_fmt', 'bgr24',
               '-vcodec', 'rawvideo']

        if self.frame_rate is not None:
            cmd += ['-r', str(self.frame_rate)]
        cmd += ['-']

        self.ffmpeg_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=self.buffer_size)

        self._state = 2

    def tearDown(self):
        if self.ffmpeg_proc is not None:
            # TODO 当子进程已经结束时，给子进程 stdin 写数据在某些环境下会出错，暂时忽略
            try:
                self.ffmpeg_proc.communicate(b'q')
            except Exception as e:
                pass
                # print(e.msg)
            self.ffmpeg_proc = None

        self._state = 3

    def next(self):
        if self._state != 2:
            raise ValueError()

        raw_frame = self.ffmpeg_proc.stdout.read(self.frame_size)
        if raw_frame is None or len(raw_frame) < self.frame_size:
            raise StopIteration()

        frame = numpy.fromstring(raw_frame, dtype='uint8')
        frame = frame.reshape((self.video_shape[1], self.video_shape[0], 3))

        self._current_frame = frame.reshape((self.video_shape[1], self.video_shape[0], 3))
        self._current_frame_num += 1
        return self._current_frame_num, self._current_frame


def si(gray_image):
    # T-REC-P.910-200804-I!!PDF-E
    # 3 x 3 kernel
    sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

    si_map = numpy.sqrt(sobelx * sobelx + sobely * sobely)

    return numpy.std(si_map), si_map


def ti(prev_image, image):
    ti_map = numpy.abs(image - prev_image)
    return numpy.std(ti_map), ti_map


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='logging verbose')

    # extract
    parser.add_argument('-r', '--frame-rate', type=float, help='frame rate')
    parser.add_argument('video_paths', nargs='+')
    args = parser.parse_args()

    frame_rate = args.frame_rate

    for video_path in args.video_paths:
        video_path = os.path.abspath(video_path)

        video_filename = os.path.basename(video_path)
        video_name = os.path.splitext(video_filename)[0]

        video_parent_dir = os.path.dirname(video_path)

        si_csv_path = os.path.join(video_parent_dir, '%s_si.csv' % (video_name, ))
        ti_csv_path = os.path.join(video_parent_dir, '%s_ti.csv' % (video_name, ))

        video_frames = VideoFrames(video_path, frame_rate=frame_rate)

        with video_frames, open(si_csv_path, 'wb') as si_file, open(ti_csv_path, 'wb') as ti_file:
            si_writer = csv.writer(si_file)
            ti_writer = csv.writer(ti_file)

            prev_frame_num = None
            prev_frame = None
            for frame_num, frame in video_frames:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                si_val, si_map = si(gray_frame)

                si_writer.writerow([frame_num, str(si_val)])

                if prev_frame_num is not None:
                    ti_val, ti_map = ti(prev_frame, frame)
                    ti_writer.writerow([prev_frame_num, frame_num, str(ti_val)])

                prev_frame_num = frame_num
                prev_frame = frame




if __name__ == "__main__":
    main()
