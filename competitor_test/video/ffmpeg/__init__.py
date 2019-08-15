# -*- coding:utf-8 -*-
import os

__author__ = 'LibX'


def _find_bin_by_path(path, exe):
    exe_path = os.path.join(path, exe)
    if os.path.exists(exe_path) and os.path.isfile(exe_path):
        return exe_path
    exe_path = os.path.join(path, '%s.exe' % (exe,))
    if os.path.exists(exe_path) and os.path.isfile(exe_path):
        return exe_path


def find_bin(bin_name):
    bin_path = None
    ffmpeg_home = os.environ.get('FFMPEG_HOME')
    if ffmpeg_home is not None:
        bin_path = _find_bin_by_path(os.path.join(ffmpeg_home, 'bin'), bin_name)
    if bin_path is not None:
        return bin_path

    path_env = os.environ.get('PATH')
    if path_env is None:
        # todo raise error
        return None

    paths = path_env.split(os.pathsep)
    for path in paths:
        bin_path = _find_bin_by_path(path, bin_name)
        if bin_path is not None:
            return bin_path
    return None
