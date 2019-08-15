# -*- coding:utf-8 -*-

import os
import subprocess
import threading
import cv2

import numpy

__author__ = 'LibX'


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


def get_audio_sample_rate(audio_path):
    ffprobe_path = find_bin('ffprobe')

    cmd = [ffprobe_path,
           '-v', 'error',
           '-show_entries', 'stream=sample_rate',
           '-of', 'default=noprint_wrappers=1',
           audio_path]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = child.communicate()

    sample_rate = None
    stdout_lines = stdout.splitlines()
    for stdout_line in stdout_lines:
        key, value = stdout_line.split('=')
        if key == 'sample_rate':
            sample_rate = int(value)

    return sample_rate


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


class DirectoryFrameGenerator(FrameGenerator):
    def __init__(self, frame_dir, frame_ext):
        super(DirectoryFrameGenerator, self).__init__()
        self.frame_dir = frame_dir
        self.frame_ext = frame_ext
        self.frame_files = None
        self.frame_index = 0

        import cv2
        self.imread = cv2.imread

    def setUp(self):
        files = [os.path.join(self.frame_dir, _)
                 for _ in os.listdir(self.frame_dir)]
        self.frame_files = [_ for _ in files if os.path.splitext(
            _)[1] == self.frame_ext and os.path.isfile(_)]
        self.frame_index = 0

    def tearDown(self):
        self.frame_files = None
        self.frame_index = 0

    def get(self):
        if self.frame_files is None:
            raise ValueError()
        if self.frame_index < 0 or self.frame_index >= len(self.frame_files):
            return None
        frame_file = self.frame_files[self.frame_index]

        frame = self.imread(frame_file)
        self.frame_index += 1
        return frame


class FrameFilter(object):
    def __init__(self):
        super(FrameFilter, self).__init__()

    def __call__(self, frame):
        return self.filter(frame)

    def filter(self, frame):
        raise NotImplementedError


class NothingFrameFilter(FrameFilter):
    def __init__(self):
        super(NothingFrameFilter, self).__init__()

    def filter(self, frame):
        return frame


class ROIFrameFilter(FrameFilter):
    def __init__(self, x, y, width, height):
        super(ROIFrameFilter, self).__init__()
        self.x, self.y, self.width, self.height = x, y, width, height

    def filter(self, frame):
        if frame is None:
            return None
        return frame[self.y:self.y + self.height, self.x:self.x + self.width]

class ResizeFrameFilter(FrameFilter):
    def __init__(self, width, height):
        super(ResizeFrameFilter, self).__init__()
        self.width, self.height = width, height

    def filter(self, frame):
        if frame is None:
            return None
        return cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_LANCZOS4)


class FilterFrameGenerator(FrameGenerator):
    def __init__(self, frame_provider, frame_filters):
        super(FilterFrameGenerator, self).__init__()
        self.frame_provider = frame_provider
        self.frame_filters = frame_filters if frame_filters is not None else []

    def setUp(self):
        self.frame_provider.setUp()

    def tearDown(self):
        self.frame_provider.tearDown()

    def get(self):
        frame = self.frame_provider.get()
        for frame_filter in self.frame_filters:
            frame = frame_filter.filter(frame)
        return frame


class FrameProducer(threading.Thread):
    def __init__(self, frame_provider):
        super(FrameProducer, self).__init__()
        self.provider = frame_provider

        self.current_frame = None
        self.lock = threading.RLock()
        self.empty_condition = threading.Condition(self.lock)
        self.full_condition = threading.Condition(self.lock)

        self.wait_step = 1
        self.is_stopping = False

    def __enter__(self):
        self.setDaemon(True)
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def run(self):
        with self.provider:
            while not self.is_stopping:
                with self.lock:
                    if self.current_frame is not None:
                        self.full_condition.wait(1)
                    else:
                        frame = self.provider.get()
                        if frame is None:
                            break

                        self.current_frame = frame
                        self.empty_condition.notify()

    def has_frame(self):
        return self.current_frame is not None

    def wait_frame(self, time):
        while time > 0:
            with self.lock:
                if self.current_frame is None:
                    self.empty_condition.wait(self.wait_step)
                else:
                    frame = self.current_frame
                    self.current_frame = None
                    self.full_condition.notify()
                    return frame
            time -= self.wait_step
        return None

    def stop(self):
        self.is_stopping = True


if __name__ == '__main__':
    ffprobe_path = find_bin('ffprobe')
    print ffprobe_path