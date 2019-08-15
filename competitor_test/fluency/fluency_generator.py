# -*- coding: utf-8 -*-

import os
import sys
import subprocess

import cv2
import numpy


# ffmpeg -framerate 1/5 -i img%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
# ffmpeg -r 60 -i frames/test%05d.bmp -c:v libx264 -r 60 -pix_fmt yuv420p fluency.mp4


def _find_bin_by_path(path, exe):
    exe_path = os.path.join(path, exe)
    if os.path.exists(exe_path) and os.path.isfile(exe_path):
        return exe_path
    exe_path = os.path.join(path, '%s.exe' % (exe,))
    if os.path.exists(exe_path) and os.path.isfile(exe_path):
        return exe_path


def find_bin(bin_name, environs=None):
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


def combine_video(video_path, frame_pattern, frame_rate):
    ffmpeg_path = find_ffmpeg()
    assert ffmpeg_path is not None

    cmd = [ffmpeg_path,
           '-r', str(frame_rate), '-i', frame_pattern,
           '-y',  # yes to all
           '-an', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(frame_rate), video_path]
    # print ' '.join(cmd)
    child = subprocess.Popen(cmd, cwd=os.path.dirname(ffmpeg_path))
    child.communicate()
    child.poll()


def draw_chessboard(board_size, cell_shape=(50, 50), border_size=(20, 20), marker_size=30, rgb=(0, 0, 0), reverse_rgb=(255, 255, 255)):
    assert len(board_size) == 2 and len(cell_shape) == 2

    board_size = numpy.array(board_size)  # (width, height)
    cell_shape = numpy.array(cell_shape)  # (width, height)
    border_size = numpy.array(border_size)  # (width, heights)

    image_shape = numpy.multiply((board_size + 1), cell_shape) + border_size * 2  # (width, height)
    image_shape = numpy.array((image_shape[1], image_shape[0], 3))  # (height, width, channels)

    image = numpy.zeros(image_shape, dtype='uint8')
    image[:, :] = reverse_rgb

    for j in range(board_size[1] + 1):
        is_odd_row = (j % 2 == 0)
        for i in range(board_size[0] + 1):
            is_odd_col = (i % 2 == 0)

            cell_color = rgb if is_odd_row == is_odd_col else reverse_rgb  # 奇行奇列或者偶行偶列
            y, x = numpy.multiply(cell_shape, (j, i)) + border_size

            image[y:y + cell_shape[0], x:x + cell_shape[1]] = cell_color

    # outer left top marker
    left_top_x, left_top_y = border_size + (cell_shape - marker_size) / 2
    right_mid_x, right_mid_y = left_top_x + marker_size, border_size[0] + cell_shape[0] / 2
    left_bottom_x, left_bottom_y = left_top_x, left_top_y + marker_size

    # inner left top marker
    # left_top_x, left_top_y = border_size + cell_shape + (cell_shape - marker_size) / 2
    # right_mid_x, right_mid_y = left_top_x + marker_size, border_size[0] + cell_shape[0] + cell_shape[0] / 2
    # left_bottom_x, left_bottom_y = left_top_x, left_top_y + marker_size

    points = numpy.array(((right_mid_x, right_mid_y), (left_top_x, left_top_y), (left_bottom_x, left_bottom_y)), numpy.int32)
    points = points.reshape((-1, 1, 2))

    cv2.fillPoly(image, [points], reverse_rgb)

    return image


def draw_progress(progress_size, progress, cell_shape=(50, 50), border_size=(20, 20), rgb=(0, 0, 0), reverse_rgb=(255, 255, 255)):
    assert len(progress_size) == 2 and len(cell_shape) == 2

    progress_size = numpy.array(progress_size)  # (width, height)
    cell_shape = numpy.array(cell_shape)  # (width, height)
    border_size = numpy.array(border_size)  # (width, height)

    image_shape = numpy.multiply(progress_size, cell_shape) + border_size * 2  # (width, height)
    image_shape = numpy.array((image_shape[1], image_shape[0], 3))  # (height, width, channels)

    image = numpy.zeros(image_shape, dtype='uint8')
    image[:, :] = rgb

    col = progress % progress_size[0]
    row = (progress / progress_size[0]) % progress_size[1]

    # print row, col

    end_x, start_y = numpy.multiply(cell_shape, (col + 1, row)) + border_size
    start_x, end_y = border_size[1], start_y + cell_shape[0]

    image[start_y:end_y, start_x:end_x] = reverse_rgb

    return image


def main():
    video_name = 'test'
    frame_type = 'bmp'
    frame_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'frames')
    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)

    video_path = os.path.join(os.path.dirname(frame_dir), video_name + '.mp4')
    frame_pattern = os.path.join(frame_dir, video_name + '%05d.' + frame_type)

    frame_shape = numpy.array((1080, 1920))
    height, width = frame_shape

    board_size = (4, 4)
    progress_size = (10, 5)
    cell_shape = (50, 50)
    marker_size = 30

    locator = draw_chessboard(board_size, cell_shape=cell_shape, marker_size=marker_size)
    progressor = draw_progress(progress_size, 0, cell_shape=cell_shape)

    start_y, start_x = (frame_shape - (max(locator.shape[0], progressor.shape[0]), locator.shape[1] + progressor.shape[1])) / 2

    black_total = 3 * 60
    content_total = 2 * 60 * 60
    total = black_total + content_total + black_total
    for i in range(total):
        frame = numpy.zeros((height, width, 3), dtype='uint8')
        frame[:, :] = (255, 255, 255)

        frame[start_y:start_y + locator.shape[0], start_x:start_x + locator.shape[1]] = locator

        if black_total <= i < black_total + content_total:
            progress = i - black_total
            progressor = draw_progress(progress_size, progress, cell_shape=cell_shape)
            frame[start_y:start_y + progressor.shape[0], start_x + locator.shape[1]:start_x + locator.shape[1] + progressor.shape[1]] = progressor

        # progressor = draw_progress(progress_size, 9, cell_shape=cell_shape)
        # frame[start_y:start_y + progressor.shape[0], start_x + locator.shape[1]:start_x + locator.shape[1] + progressor.shape[1]] = progressor

        # cv2.imshow('test', frame)
        # cv2.waitKey()
        # exit(0)

        frame_filepath = frame_pattern % (i + 1,)

        cv2.imwrite(frame_filepath, frame)

    combine_video(video_path, frame_pattern, 60)

if __name__ == '__main__':
    main()