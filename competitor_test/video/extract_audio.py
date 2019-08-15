# -*- coding:utf-8 -*-

import argparse
import os
import subprocess

import ffmpeg

__author__ = 'LibX'


def extract_audio(video_path, audio_path):
    ffmpeg_path = ffmpeg.find_bin('ffmpeg')

    #cmd = [ffmpeg_path, '-i', video_path, '-vn', '-acodec', 'copy', audio_path]
    cmd = [ffmpeg_path, '-i', video_path, '-y', '-vn', audio_path]
    child = subprocess.Popen(cmd)
    child.wait()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('--output-dir', help='output dir')
    parser.add_argument('video_paths', nargs='+')
    args = parser.parse_args()

    for video_path in args.video_paths:
        video_file = os.path.basename(video_path)
        video_name = os.path.splitext(video_file)[0]

        video_dir = os.path.dirname(video_path) if args.output_dir is None else args.output_dir
        audio_path = os.path.join(video_dir, '%s.wav' % (video_name,))

        extract_audio(video_path,audio_path)


if __name__ == "__main__":
    main()