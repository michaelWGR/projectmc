# -*- coding:utf-8 -*-

import argparse
import os

import cv2
import numpy
import subprocess
# from utils import get_video_shape, VideoFrameGenerator


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
    print(stdout)
    print(_)
    video_info= json.loads(stdout)
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

class FrameGenerator(object):
    def __init__(self):
        super(FrameGenerator, self).__init__()

    def __enter__(self):
        self.setUp()
        while True:
            frame = self.get()
            if frame is None:
                break
            yield frame

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tearDown()

    def setUp(self):
        raise NotImplementedError()

    def tearDown(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()


class VideoFrameGenerator(FrameGenerator):
    def __init__(self, video_path, video_shape, frame_rate, buffer_size=None):
        super(VideoFrameGenerator, self).__init__()
        self.video_path = video_path
        self.video_shape = video_shape
        self.frame_rate = frame_rate

        self.frame_size = self.video_shape[0] * self.video_shape[1] * 3

        self.ffmpeg_path = find_bin('ffmpeg')
        self.ffmpeg_proc = None
        self.buffer_size = buffer_size if buffer_size is not None else self.frame_size * 10

    def setUp(self):
        cmd = [self.ffmpeg_path,
               '-i', self.video_path,
               '-f', 'image2pipe',
               '-pix_fmt', 'bgr24',
               '-vcodec', 'rawvideo']

        if self.frame_rate is not None:
            cmd += ['-r', str(self.frame_rate)]
        cmd += ['-']

        self.ffmpeg_proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=self.buffer_size)

    # def tearDown(self):
    #     if self.ffmpeg_proc is not None:
    #         self.ffmpeg_proc.communicate('q')
    #         # self.ffmpeg_proc.terminate()
    #         self.ffmpeg_proc.poll()
    #         self.ffmpeg_proc = None

    def tearDown(self):
        if self.ffmpeg_proc is not None:
            # TODO 当子进程已经结束时，给子进程 stdin 写数据在某些环境下会出错，暂时忽略
            try:
                self.ffmpeg_proc.communicate(b'q')
            except Exception as e:
                pass
                # print(e.msg)
            self.ffmpeg_proc = None

    def get(self):
        raw_frame = self.ffmpeg_proc.stdout.read(self.frame_size)
        if raw_frame is None or len(raw_frame) < self.frame_size:
            return None
        frame = numpy.fromstring(raw_frame, dtype='uint8')
        frame = frame.reshape((self.video_shape[1], self.video_shape[0], 3))
        return frame


def extract_frame(video_path, video_shape, frames_dir, frame_rate=None, distinct=False, frame_nums=None, frame_type='jpg'):
    video_file = os.path.basename(video_path)
    video_name = os.path.splitext(video_file)[0]
    frames_file_pattern = os.path.join(frames_dir, video_name + '%05d.' + frame_type)
    
    if frame_nums is None:
        frame_generator = VideoFrameGenerator(video_path, video_shape, frame_rate)
        with frame_generator as frames:
            i = 1
            prev_frame = None
            for frame in frames:
                should_write = True
                if prev_frame is not None and distinct:
                    should_write = not numpy.array_equal(prev_frame, frame)
                    
                if should_write:
                    cv2.imwrite(frames_file_pattern % (i,), frame)
                prev_frame = frame
                i += 1
    else:
        frame_nums = sorted(frame_nums)
        max_frame_num = max(frame_nums)

        frame_generator = VideoFrameGenerator(video_path, video_shape, frame_rate)
        with frame_generator as frames:
            frame_num_index = 0
            frame_num = frame_nums[frame_num_index]
            i = 1

            for frame in frames:
                should_write = False
                if frame_nums is None:
                    # no frame_nums, write all
                    should_write = True
                else:
                    if i > max_frame_num:
                        break

                    if i == frame_num:
                        should_write = True
                        frame_num_index += 1
                        if frame_num_index < len(frame_nums):
                            frame_num = frame_nums[frame_num_index]

                if should_write:
                    cv2.imwrite(frames_file_pattern % (i,), frame)

                i += 1


def get_file_path(files_path):
    path_list = []
    if os.path.isfile(files_path):
        path_list.append(files_path)
        return path_list

    for root,dirs,files in os.walk(files_path):
        for item in files:
            if os.path.splitext(item)[1] != '' and (item.endswith('.mp4') or item.endswith('.mkv') or item.endswith('.flv') or item.endswith('.MOV')):
                file_path = os.path.join(files_path,item)
                path_list.append(file_path)
        return path_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', type=float, help='frame rate')
    parser.add_argument('-d', '--distinct', action='store_true', default=False, help='distinct')
    parser.add_argument('-n', '--frame-nums', nargs='*', type=int, help='frame nums')
    parser.add_argument('-t', '--frame-type', help='frame type')
    parser.add_argument('--output-dir', help='output dir')
    parser.add_argument('video_paths')
    args = parser.parse_args()

    frame_rate = args.frame_rate
    distinct = args.distinct
    frame_nums = args.frame_nums if args.frame_nums is not None and len(args.frame_nums) > 0 else None
    frame_type = args.frame_type if args.frame_type is not None else 'jpg'

    file_path_list = get_file_path(args.video_paths)

    for video_path in file_path_list:
        video_path = os.path.abspath(video_path)
        video_file = os.path.basename(video_path)
        video_name = os.path.splitext(video_file)[0]

        frames_dir = args.output_dir
        if frames_dir is None:
            frames_basedir = os.path.dirname(video_path)
            frames_dir = os.path.join(frames_basedir, video_name)

            if not os.path.exists(frames_dir):
                os.mkdir(frames_dir)

        video_shape = get_video_shape(video_path)
        extract_frame(video_path, video_shape, frames_dir, frame_rate=frame_rate, distinct=distinct, frame_nums=frame_nums, frame_type=frame_type)


if __name__ == "__main__":
    main()
