# -*- coding: utf-8 -*-

import os
import sys
import datetime
import csv
import math
import argparse
import subprocess
import weakref

import cv2
import numpy

import logging


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


class Debug(object):
    is_debug = False
    frame_num = 1
    frame_show = False
    has_frame_show = False

    def __init__(self):
        raise ValueError()

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument('-d', '--frame-debug', action='store_true', default=False, help='debug')
        parser.add_argument('-n', '--frame-num', type=int, default=1, help='debug frame num')
        parser.add_argument('--show-frame', action='store_true', default=False, help='debug frame show')

    @classmethod
    def parse(cls, args):
        cls.is_debug = args.frame_debug
        if cls.is_debug:
            logging.info('debug mode is turn on')
        cls.frame_num = args.frame_num
        cls.frame_show = args.show_frame


def get_frame_dir(video_path, output_base_dir=None):
    video_path = os.path.abspath(video_path)
    video_file_name = os.path.basename(video_path)
    video_name = os.path.splitext(video_file_name)[0]
    video_parent_dir = os.path.dirname(video_path)

    output_base_dir = video_parent_dir if output_base_dir is None else output_base_dir
    return os.path.join(output_base_dir, video_name)


def get_frame_num(frame_filepath):
    frame_filename = os.path.basename(frame_filepath)
    frame_name = os.path.splitext(frame_filename)[0]
    return int(frame_name[-7:])


def listdir_sorted(path):
    return sorted(os.listdir(path))


class FrameExtractor(object):
    VALID_EXT = ('.avi', '.mp4', '.mov', '.flv')

    def __init__(self, path, frame_rate, output_base_dir=None, frame_type='bmp'):
        self.path = os.path.abspath(path)

        if os.path.isfile(self.path):
            if os.path.splitext(self.path)[1].lower() not in self.VALID_EXT:
                raise ValueError()

            self.type = 'video'
            self.video_path = self.path

            video_file_name = os.path.basename(self.video_path)
            self.video_name = os.path.splitext(video_file_name)[0]

            self.frame_dir = get_frame_dir(self.video_path, output_base_dir=output_base_dir)
        elif os.path.isdir(self.path):
            self.type = 'frames'
            self.video_path = None

            self.frame_dir = os.path.abspath(path)

            video_file_name = os.path.basename(self.frame_dir)
            self.video_name = os.path.splitext(video_file_name)[0]
        else:
            raise ValueError()

        self.frame_rate = frame_rate
        self.frame_type = frame_type

        self.frame_pattern = os.path.join(self.frame_dir, self.video_name + '%07d.' + frame_type)

    def extract(self):
        if not self.type == 'video':
            logging.info('%s is a directory, ignore extracting', self.path)
            return None

        ffmpeg_path = find_ffmpeg()

        if ffmpeg_path is None:
            raise ValueError()

        if not os.path.exists(self.frame_dir):
            os.makedirs(self.frame_dir)

        cmd = [ffmpeg_path,
               '-i', self.video_path,
               '-r', str(self.frame_rate),
               '-f', 'image2',
               self.frame_pattern]

        child = subprocess.Popen(cmd, cwd=os.path.dirname(ffmpeg_path))

        child.communicate()
        child.poll()

        return None

    def get_frame_filepath_by_num(self, frame_num):
        return (frame_filepath for frame_filepath in self.get_frame_filepaths()
                if get_frame_num(frame_filepath) == frame_num)

    def get_frame_filepaths(self):
        frame_ext = '.' + self.frame_type

        return (os.path.join(self.frame_dir, _) for _ in listdir_sorted(self.frame_dir) if
                os.path.isfile(os.path.join(self.frame_dir, _)) and os.path.splitext(_)[1].lower() == frame_ext)


def vector_normalized(v):
    l = numpy.linalg.norm(v)
    if l < 1e-7:
        return numpy.zeros((2,))
    n = v / l
    return n


def draw_arrow(image, p1, p2, color, thickness, arrow_length):
    cv2.line(image, p1, p2, color, thickness=thickness)

    xn, yn = vector_normalized((p2[0] - p1[0], p2[1] - p1[1]))

    k = arrow_length / 1.41421356237
    cv2.line(image, p2, (int(p2[0] + ( k * ( -xn + yn ) )), int(p2[1] + ( k * ( -yn - xn ) ))), color, thickness=thickness)
    cv2.line(image, p2, (int(p2[0] + ( k * ( -xn - yn ) )), int(p2[1] + ( k * ( -yn + xn ) ))), color, thickness=thickness)


class ProgressDetector(object):
    INVALID_RESULT = (-1, -1)

    class LoggerAdapter(logging.LoggerAdapter):
        def __init__(self, logger, detector):
            super(ProgressDetector.LoggerAdapter, self).__init__(logger, {'detector_ref': weakref.ref(detector)})

        def process(self, msg, kwargs):
            detector_ref = self.extra['detector_ref']

            detector = detector_ref() if detector_ref is not None else None
            frame_name = detector.current_frame_name if detector is not None else None
            if not frame_name:
                frame_name = 'unknown'

            return '[frame:%s] %s' % (frame_name, msg), kwargs

    def __init__(self, src_frame_shape, board_size, progress_size, cell_shape, border_size, marker_size,
                 binary_threshold=None,
                 write_border_size=20):
        self.src_frame_shape = numpy.array(src_frame_shape)

        self.board_size = numpy.array(board_size)
        self.progress_size = numpy.array(progress_size)

        self.cell_shape = numpy.array(cell_shape)

        self.border_size = numpy.array(border_size)
        self.marker_size = marker_size

        self.binary_threshold = binary_threshold

        self.write_border_size = write_border_size

        self.src_locator_shape = numpy.multiply((self.board_size + 1), self.cell_shape) + self.border_size * 2  # (width, height)
        self.locator_corners = []
        for j in range(board_size[1]):
            for i in range(board_size[0]):
                src_corner = border_size + numpy.multiply((i + 1, j + 1), cell_shape)
                self.locator_corners.append(src_corner)

        # 顶点是指左上、右上、右下、左下这4个点
        self.locator_vertex_pair_indexes = ((0, 0),  # 左上
                                            (0, board_size[0] - 1),  # 右上
                                            (board_size[1] - 1, board_size[0] - 1),  # 右下
                                            (board_size[1] - 1, 0),  # 左下
                                            )
        self.locator_vertex_indexes = tuple(j * board_size[0] + i for j, i in self.locator_vertex_pair_indexes)

        # outer
        self.locator_vertex_rects = (
            (
                self.locator_corners[self.locator_vertex_indexes[0]] - self.cell_shape,
                self.locator_corners[self.locator_vertex_indexes[0]],
            ),  # 左上
            (
                self.locator_corners[self.locator_vertex_indexes[1]] - (0, self.cell_shape[1]),
                self.locator_corners[self.locator_vertex_indexes[1]] + (self.cell_shape[0], 0),
            ),  # 右上
            (
                self.locator_corners[self.locator_vertex_indexes[2]],
                self.locator_corners[self.locator_vertex_indexes[2]] + self.cell_shape,
            ),  # 右下
            (
                self.locator_corners[self.locator_vertex_indexes[3]] - (self.cell_shape[0], 0),
                self.locator_corners[self.locator_vertex_indexes[3]] + (0, self.cell_shape[1]),
            ),  # 左下
        )

        # inner
        # self.locator_vertex_rects = (
        #     (
        #         self.locator_corners[self.locator_vertex_indexes[0]],
        #         self.locator_corners[self.locator_vertex_indexes[0]] + self.cell_shape,
        #     ),  # 左上
        #     (
        #         self.locator_corners[self.locator_vertex_indexes[1]] - (self.cell_shape[0], 0),
        #         self.locator_corners[self.locator_vertex_indexes[1]] + (0, self.cell_shape[1]),
        #     ),  # 右上
        #     (
        #         self.locator_corners[self.locator_vertex_indexes[2]] - self.cell_shape,
        #         self.locator_corners[self.locator_vertex_indexes[2]],
        #     ),  # 右下
        #     (
        #         self.locator_corners[self.locator_vertex_indexes[3]] - (0, self.cell_shape[1]),
        #         self.locator_corners[self.locator_vertex_indexes[3]] + (self.cell_shape[0], 0),
        #     ),  # 左下
        # )

        self.find_locator_flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS

        # direction marker
        marker_left_top_x, marker_left_top_y = (self.cell_shape - self.marker_size) / 2
        self.marker_white_vertexes = ((marker_left_top_x, marker_left_top_y),
                                      (self.cell_shape[0] - marker_left_top_x, marker_left_top_y),
                                      (self.cell_shape[0] - marker_left_top_x, self.cell_shape[1] - marker_left_top_y),
                                      (marker_left_top_x, self.cell_shape[1] - marker_left_top_y))

        # progressor
        self.progressor_shape = numpy.multiply(self.progress_size, self.cell_shape) + numpy.array(self.border_size) * 2
        self.progressor_vertexes = numpy.float32(((0, 0), (self.progressor_shape[0], 0),
                                                  (self.progressor_shape[0], self.progressor_shape[1]),
                                                  (0, self.progressor_shape[1])))

        # 利用中心点判断
        self.progressor_left_top_cell_center = (cell_shape / 2) + border_size
        self.progressor_right_bottom_cell_center = (self.progressor_left_top_cell_center +
                                                    numpy.multiply(self.cell_shape, self.progress_size - 1))

        # 利用中心正方形判断
        self.progressor_cell_border_size = numpy.array((10, 10))
        # self.progressor_left_top_cell_left_top = self.progressor_cell_border_size + border_size
        # self.progressor_right_bottom_cell_left_top = (self.progressor_left_top_cell_left_top +
        #                                               numpy.multiply(self.cell_shape, self.progress_size - 1))

        # progressor_cell_centers = []
        # for j in range(self.progress_size[1]):
        #     for i in range(self.progress_size[0]):
        #         cell_center = numpy.multiply(cell_shape, (i, j)) + (cell_shape / 2) + border_size
        #         progressor_cell_centers.append(cell_center)
        #
        # self.progressor_cell_centers = numpy.array(progressor_cell_centers).reshape((self.progress_size[1], self.progress_size[0], 2))

        # roi = locator + progressor
        self.roi_shape = numpy.array((
            self.src_locator_shape[0] + self.progressor_shape[0],
            max(self.src_locator_shape[1], self.progressor_shape[1])))
        self.src_locator_start_y, self.src_locator_start_x = (
            self.src_frame_shape - (max(self.src_locator_shape[1], self.src_locator_shape[1]), self.src_locator_shape[0] + self.src_locator_shape[0])
            ) / 2

        # logging
        self.default_logger = logging.getLogger()
        self.logger = self.LoggerAdapter(self.default_logger, self)
        self.current_frame_name = None

        # debug
        self.has_frame_show = False

    def imshow(self, winname, mat):
        cv2.imshow(winname, mat)
        self.has_frame_show = True

    def waitKey(self, delay=None):
        if self.has_frame_show:
            delay = delay if delay is not None else 0
            cv2.waitKey(delay)

    def set_frame_name(self, frame_name):
        self.current_frame_name = frame_name

    def threshold(self, image):
        if self.binary_threshold is None:
            # 二值化
            return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        else:
            return cv2.threshold(image, self.binary_threshold, 255, cv2.THRESH_BINARY)

    def find_direction_marker(self, marker_bins):
        # 通过中点判断，只要中点是白色，就是方向标记
        center_x, center_y = self.cell_shape / 2
        self.logger.debug('center of marker (%d, %d)', center_x, center_y)

        for i in range(len(marker_bins)):
            self.logger.debug('try marker %d', i)
            marker_bin = marker_bins[i]

            if Debug.is_debug:
                self.imshow('marker %d bin' % (i,), marker_bin)

            if 255 == marker_bin[center_y, center_x]:
                self.logger.debug('center of marker %d is white, it maybe a direction marker', i)
                return i

            self.logger.debug('center of marker %d is not white, try next one', i)

        return -1

    def find_white_edge(self, direction_marker):
        self.logger.debug('---------- find_white_edge ----------')

        invert_marker = 255 - direction_marker
        marker_with_border = cv2.copyMakeBorder(invert_marker, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)
        if Debug.is_debug:
            debug_marker = cv2.cvtColor(marker_with_border, cv2.COLOR_GRAY2BGR)

        contours_img = numpy.copy(marker_with_border)
        # contours, hierarchy = cv2.findContours(contours_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(contours_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        min_square_perimeter = (direction_marker.shape[0] + direction_marker.shape[0]) * 2 * 0.8
        min_triangle_perimeter = self.marker_size * 3.23606797749979 * 0.8  # marker_perimeter = marker_size * (1 + sqrt(5))

        candicate_squares = []
        candicate_triangles = []
        for i in range(len(contours)):
            contour = contours[i]
            parent_index = hierarchy[0][i][3]

            perimeter = cv2.arcLength(contour, True)

            epsilon = 0.1 * perimeter
            approx_curve = cv2.approxPolyDP(contour, epsilon, True)

            if 4 == len(approx_curve) and perimeter >= min_square_perimeter:
                candicate_squares.append([i, parent_index, contour, approx_curve])
            elif 3 == len(approx_curve) and perimeter >= min_triangle_perimeter:
                candicate_triangles.append([i, parent_index, contour, approx_curve])

        # TODO 如果有多个?
        if len(candicate_squares) != 1 or len(candicate_triangles) != 1:
            self.logger.debug('can not find square and triangle')
            return -1

        candicate_square = candicate_squares[0]
        candicate_triangle = candicate_triangles[0]

        if candicate_triangle[1] != candicate_square[0]:
            self.logger.debug('square does not contain triangle')
            return -1

        square = candicate_square[3]
        triangle = candicate_triangle[3]
        
        if Debug.is_debug:
            cv2.circle(debug_marker, tuple(triangle[0][0]), 5, (255, 0, 0), thickness=2)
            cv2.circle(debug_marker, tuple(triangle[1][0]), 5, (0, 255, 0), thickness=2)
            cv2.circle(debug_marker, tuple(triangle[2][0]), 5, (0, 0, 255), thickness=2)

        white_triangles = []
        for i in range(3):
            j, k = (i + 1) % 3, (i + 2) % 3

            dx = triangle[j][0][0] - triangle[i][0][0]
            dy = triangle[j][0][1] - triangle[i][0][1]
            dl = math.sqrt(dx * dx + dy * dy)

            # 与x轴的夹角为xt
            sin_xt = abs(dy) / dl
            # 与y轴的夹角为yt
            sin_yt = abs(dx) / dl

            # print i, triangle[i][0], j, triangle[j][0], k, triangle[k][0], cos_t
            self.logger.debug('i=%d, %s, j=%d, %s, k=%d, %s, sin(xt)=%f, sin(yt)=%f', i, triangle[i][0], j, triangle[j][0], k, triangle[k][0], sin_xt, sin_yt)
            white_triangle = {
                'index': i,
                'approx_curve': [triangle[i], triangle[j], triangle[k]],
                'sin_xt': sin_xt,
                'sin_yt': sin_yt
            }
            white_triangles.append(white_triangle)

        # 用夹角最小的那个
        edge_angles = [min(white_triangle['sin_xt'], white_triangle['sin_yt']) for white_triangle in white_triangles]
        min_index = numpy.argmin(edge_angles)
        candicate_white_triangle = white_triangles[min_index]

        result = -1
        if candicate_white_triangle and candicate_white_triangle['approx_curve']:
            self.logger.debug('candicate white triangle is %d', candicate_white_triangle['index'])

            sin_xt = candicate_white_triangle['sin_xt']
            sin_yt = candicate_white_triangle['sin_yt']
            approx_curve = candicate_white_triangle['approx_curve']
            mx, my = (approx_curve[0][0][0] + approx_curve[1][0][0]) / 2, (approx_curve[0][0][1] + approx_curve[1][0][1]) / 2

            if Debug.is_debug:
                draw_arrow(debug_marker, tuple(approx_curve[0][0]), tuple(approx_curve[1][0]), (255, 0, 0), 2, 10)
                draw_arrow(debug_marker, (mx, my), tuple(approx_curve[2][0]), (0, 255, 0), 2, 10)

            if sin_xt <= sin_yt:  # TODO 其实是不能接受相等这个条件的
                # 与x轴平行, 白边在上或者在下
                if my < approx_curve[2][0][1]:
                    # 白边在上
                    result = 0
                elif my > approx_curve[2][0][1]:
                    # 白边在下
                    result = 2
            else:
                # 与y轴平行, 白边在左或者在右
                if mx < approx_curve[2][0][0]:
                    # 白边在左
                    result = 3
                elif mx > approx_curve[2][0][0]:
                    # 白边在右
                    result = 1

        if Debug.is_debug and Debug.frame_show:
            self.imshow('Marker with direction', debug_marker)

        return result

        # # 通过方向标记三角形的顶点判断白边所在位置
        # white_vertexes_bit = [255 == direction_marker[white_points[1], white_points[0]]
        #                       for white_points in self.marker_white_vertexes]
        # if white_vertexes_bit[0] and white_vertexes_bit[1]:
        #     return 0  # 白边在上
        # elif white_vertexes_bit[1] and white_vertexes_bit[2]:
        #     return 1  # 白边在右
        # elif white_vertexes_bit[2] and white_vertexes_bit[3]:
        #     return 2  # 白边在下
        # elif white_vertexes_bit[3] and white_vertexes_bit[0]:
        #     return 3  # 白边在左

        # return -1

    def fix_locator_corners_order(self, target_locator_corners, marker_index, white_edge_index):
        self.logger.debug('---------- fix_locator_corners_order ----------')
        # 方向标记位置(marker_index)有4种情况，白边位置(white_edge_index)有4种情况
        # 即一共有16种情况，但只有8种情况是正常情况，可以通过翻转+旋转的方式达到
        ordered_locator_corners = []

        self.logger.debug('marker_index is %d, white_edge_index is %d', marker_index, white_edge_index)
        if 0 == marker_index:  # 方向标记在左上
            if 0 == white_edge_index:  # 白边在上
                self.logger.debug('flip y and rot -90')
                # flip y and rot -90

                # example:
                # src board_size=(4, 3), 3 rows 4 cols
                # src A(0, 0)=>[0] B(0, 3)=>[3] C(2, 3)=>[11] D(2, 0)=>[8]
                # target board_size=(3, 4), 4 rows 3 cols
                # target A(0, 0)=>[0] B(3, 0)=>[9] C(3, 2)=>[11] D(0, 2)=>[2]
                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        j = src_i
                        i = src_j

                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, j, i)

                        index = j * self.board_size[1] + i

                        ordered_locator_corners.append(target_locator_corners[index])
            elif 3 == white_edge_index:  # 白边在左
                self.logger.debug('nothing to do')
                # nothing to do
                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, src_j, src_i)

                        index = src_j * self.board_size[0] + src_i
                        ordered_locator_corners.append(target_locator_corners[index])
        elif 1 == marker_index:  # 方向标记在右上
            if 0 == white_edge_index:  # 白边在上
                self.logger.debug('rot -90')
                # rot -90

                # example:
                # src board_size=(4, 3), 3 rows 4 cols
                # src A(0, 0)=>[0] B(0, 3)=>[3] C(2, 3)=>[11] D(2, 0)=>[8]
                # target board_size=(3, 4), 4 rows 3 cols
                # target A(0, 2)=>[2] B(3, 2)=>[11] C(3, 0)=>[9] D(0, 0)=>[0]

                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        j = src_i
                        i = self.board_size[1] - 1 - src_j

                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, j, i)

                        index = j * self.board_size[1] + i

                        ordered_locator_corners.append(target_locator_corners[index])
            elif 1 == white_edge_index:  # 白边在右
                self.logger.debug('flip y')
                # flip y

                # example:
                # src board_size=(4, 3), 3 rows 4 cols
                # src A(0, 0)=>[0] B(0, 3)=>[3] C(2, 3)=>[11] D(2, 0)=>[8]
                # target board_size=(4, 3), 3 rows 4 cols
                # target A(0, 3)=>[3] B(0, 0)=>[0] C(2, 0)=>[8] D(2, 3)=>[11]

                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        j = src_j
                        i = self.board_size[0] - 1 - src_i

                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, j, i)

                        index = j * self.board_size[0] + i

                        ordered_locator_corners.append(target_locator_corners[index])
        elif 2 == marker_index:  # 方向标记在右下
            if 1 == white_edge_index:  # 白边在右
                self.logger.debug('rot 180')
                # rot 180

                # example:
                # src board_size=(4, 3), 3 rows 4 cols
                # src A(0, 0)=>[0] B(0, 3)=>[3] C(2, 3)=>[11] D(2, 0)=>[8]
                # target board_size=(4, 3), 3 rows 4 cols
                # target A(2, 3)=>[11] B(2, 0)=>[8] C(0, 0)=>[0] D(0, 3)=>[3]
                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        j = self.board_size[1] - 1 - src_j
                        i = self.board_size[0] - 1 - src_i

                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, j, i)

                        index = j * self.board_size[0] + i

                        ordered_locator_corners.append(target_locator_corners[index])
            elif 2 == white_edge_index:  # 白边在下
                self.logger.debug('flip y and rot 90')
                # flip y and rot 90

                # example:
                # src board_size=(4, 3), 3 rows 4 cols
                # src A(0, 0)=>[0] B(0, 3)=>[3] C(2, 3)=>[11] D(2, 0)=>[8]
                # target board_size=(3, 4), 4 rows 3 cols
                # target A(3, 2)=>[11] B(0, 2)=>[2] C(0, 0)=>[0] D(3, 0)=>[9]
                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        j = self.board_size[0] - 1 - src_i
                        i = self.board_size[1] - 1 - src_j

                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, j, i)

                        index = j * self.board_size[1] + i

                        ordered_locator_corners.append(target_locator_corners[index])
        elif 3 == marker_index:  # 方向标记在左下
            if 2 == white_edge_index:  # 白边在下
                self.logger.debug('rot 90')
                # rot 90

                # example:
                # src board_size=(4, 3), 3 rows 4 cols
                # src A(0, 0)=>[0] B(0, 3)=>[3] C(2, 3)=>[11] D(2, 0)=>[8]
                # target board_size=(3, 4), 4 rows 3 cols
                # target A(3, 0)=>[9] B(0, 0)=>[0] C(0, 2)=>[2] D(3, 2)=>[11]
                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        j = self.board_size[0] - 1 - src_i
                        i = src_j

                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, j, i)

                        index = j * self.board_size[1] + i

                        ordered_locator_corners.append(target_locator_corners[index])
            elif 3 == white_edge_index:  # 白边在左
                self.logger.debug('flip x')
                # flip x

                # example:
                # src board_size=(4, 3), 3 rows 4 cols
                # src A(0, 0)=>[0] B(0, 3)=>[3] C(2, 3)=>[11] D(2, 0)=>[8]
                # target board_size=(4, 3), 3 rows 4 cols
                # target A(2, 0)=>[8] B(2, 3)=>[11] C(0, 3)=>[3] D(0, 0)=>[0]
                for src_j in range(self.board_size[1]):
                    for src_i in range(self.board_size[0]):
                        j = self.board_size[1] - 1 - src_j
                        i = src_i

                        self.logger.debug('src (%d, %d) => target (%d, %d)', src_j, src_i, j, i)

                        index = j * self.board_size[0] + i

                        ordered_locator_corners.append(target_locator_corners[index])

        return ordered_locator_corners if ordered_locator_corners else None

    def get_progressor_matrix(self, binary_progressor):
        # 利用中心点判断
        # left_top_x, left_top_y = self.progressor_left_top_cell_center
        # right_bottom_x, right_bottom_y = self.progressor_right_bottom_cell_center

        # progressor_centers_gray = binary_progressor[left_top_y:right_bottom_y + 1:self.cell_shape[1],
        #                                             left_top_x:right_bottom_x + 1:self.cell_shape[0]]

        # return numpy.where(progressor_centers_gray == 255, 1, 0)

        # 利用中心正方形判断
        result = numpy.zeros((self.progress_size[1], self.progress_size[0]), dtype='uint8')
        for i in range(self.progress_size[0]):
            left_top_x = self.progressor_cell_border_size[0] + self.border_size[0] + i * self.cell_shape[0]
            right_bottom_x = left_top_x + self.cell_shape[0] - 2 * self.progressor_cell_border_size[0]
            for j in range(self.progress_size[1]):
                left_top_y = self.progressor_cell_border_size[1] + self.border_size[1] + j * self.cell_shape[1]
                right_bottom_y = left_top_y + self.cell_shape[1] - 2 * self.progressor_cell_border_size[1]

                cell = binary_progressor[left_top_y:right_bottom_y, left_top_x:right_bottom_x]
                # print left_top_y, right_bottom_y, left_top_x, right_bottom_x
                # print i, j, cell
                # cv2.imshow('shit', cell)
                # cv2.waitKey(0)

                white_percent = numpy.average(numpy.where(cell == 255, 1, 0))
                result[j, i] = int(1 if white_percent > 0.9 else 0)

        return result

    def has_progressor(self, progressor, progressor_threshold):
        # 二值化后，四周添加白边，再通过轮廓检测，获取第二层轮廓即我们需要找到的进度条轮廓
        gray_progressor = cv2.cvtColor(progressor, cv2.COLOR_BGR2GRAY)
        progressor_threshold, binary_progressor = cv2.threshold(gray_progressor,
                                                                progressor_threshold, 255, cv2.THRESH_BINARY)

        # white_percent = numpy.sum(numpy.where(binary_progressor == 255, 1, 0)) / float(binary_progressor.shape[0] * binary_progressor.shape[1])
        # return white_percent < 0.5

        progressor_matrix = self.get_progressor_matrix(binary_progressor)
        return numpy.sum(progressor_matrix) < (progressor_matrix.shape[0] * progressor_matrix.shape[1]) / 3

    def find_progressor_vertexes(self, progressor, progressor_threshold):
        # 二值化后，四周添加白边，再通过轮廓检测，获取第二层轮廓即我们需要找到的进度条轮廓
        gray_progressor = cv2.cvtColor(progressor, cv2.COLOR_BGR2GRAY)
        progressor_threshold, binary_progressor = cv2.threshold(gray_progressor, progressor_threshold, 255, cv2.THRESH_BINARY)
        self.logger.debug('binary threshold progressor with %d', progressor_threshold)
        # _, binary_progressor = cv2.threshold(gray_progressor, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary_progressor = cv2.copyMakeBorder(binary_progressor,
                                               self.write_border_size, self.write_border_size,
                                               self.write_border_size, self.write_border_size,
                                               cv2.BORDER_CONSTANT, value=255)
        if Debug.is_debug:
            self.imshow('binary progressor', binary_progressor)
        contours, hierarchy = cv2.findContours(binary_progressor, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        self.logger.debug('%d contours found', len(contours))

        target_index = -1
        for i in range(len(hierarchy[0])):
            hierarchy_item = hierarchy[0][i]

            level = 0
            while hierarchy_item[3] >= 0:
                j = hierarchy_item[3]
                hierarchy_item = hierarchy[0][j]
                level += 1

            if hierarchy_item[3] < 0:
                level += 1

            self.logger.debug('contour %d level %d', i, level)
            if 2 == level:
                target_index = i
                break

        if target_index < 0:
            return None

        self.logger.debug('contour %d is progressor contour', target_index)

        # 进行多边形拟合，缩减到4个顶点
        self.logger.debug('approxPolyDP with contour %d', target_index)
        epsilon = 0.1 * cv2.arcLength(contours[target_index], True)
        approx = cv2.approxPolyDP(contours[target_index], epsilon, True)

        if approx.shape[0] != 4:
            self.logger.warning('approx contour %d is not a quadrilateral, but a %d-poly', target_index, approx.shape[0])
            return None

        area = cv2.contourArea(approx)
        if area < gray_progressor.shape[0] * gray_progressor.shape[1] / 16:
            self.logger.warning('approx contour %d is too small', target_index)
            return None

        # 为4个顶点进行排序
        vertexes = approx.reshape((4, 2)) - (self.write_border_size, self.write_border_size)

        # 距离左上距离最近的点，即左上顶点
        left_top_index = numpy.argmin(list(numpy.linalg.norm(vertex) for vertex in vertexes))

        # 距离右上距离最近的点，即右上顶点
        right_top_index = numpy.argmin(list(numpy.linalg.norm(vertex)
                                            for vertex in (vertexes - (self.progressor_shape[0], 0))))

        step = right_top_index - left_top_index
        if step == 3:
            step = -1
        elif step == -3:
            step = 1

        if not step == -1 and not step == 1:
            self.logger.warning('approx contour %d has sth. wrong', target_index)
            return None

        vertexes = numpy.concatenate((vertexes[left_top_index::step], vertexes[:left_top_index:step]))
        return numpy.array(vertexes)

    def detect(self, target_frame, frame_name=None):
        try:
            self.current_frame_name = frame_name
            return self._detect(target_frame)
        except Exception:
            self.logger.exception('detect frame error')
            return self.INVALID_RESULT
        finally:
            self.current_frame_name = None
            if Debug.is_debug and Debug.frame_show:
                self.waitKey()

    def _detect(self, target_frame):
        if Debug.is_debug:
            debug_frame = numpy.copy(target_frame)

            if Debug.frame_show:
                self.imshow('frame', debug_frame)

        self.logger.debug('try to find locator, size %s', tuple(self.board_size))
        gray_frame = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)
        # 找棋盘，获取棋盘的内部角点

        for blur_kernel_size in range(1, 7, 2):
            if blur_kernel_size > 1:
                # 可能有噪点影响
                # 使用模糊去噪
                self.logger.debug('try kernel size %d' % (blur_kernel_size,))
                blur_frame = cv2.blur(gray_frame, (blur_kernel_size, blur_kernel_size))
            else:
                blur_frame = gray_frame

            target_locator_found, target_locator_corners = cv2.findChessboardCorners(blur_frame, tuple(self.board_size),
                                                                                     flags=self.find_locator_flags)

            if target_locator_found:
                self.logger.debug('can not find locator')

        if not target_locator_found:
            self.logger.debug('can not find locator, size %s', tuple(self.board_size))
            return self.INVALID_RESULT

        self.logger.debug('locator found, size %s', tuple(self.board_size))
        if self.logger.isEnabledFor(logging.DEBUG):
            for i in range(len(target_locator_corners)):
                self.logger.debug('locator corner %d %s', i, tuple(target_locator_corners[i][0]))

        # 精确定位棋盘的内部角点
        self.logger.debug('corner sub pix')
        cv2.cornerSubPix(gray_frame, target_locator_corners, (11, 11), (-1, -1),
                         (cv2.cv.CV_TERMCRIT_EPS + cv2.cv.CV_TERMCRIT_ITER, 30, 0.1))
        if self.logger.isEnabledFor(logging.DEBUG):
            for i in range(len(target_locator_corners)):
                self.logger.debug('locator sub pix corner %d %s', i, tuple(target_locator_corners[i][0]))

        if Debug.is_debug and Debug.frame_show:
            cv2.drawChessboardCorners(debug_frame, tuple(self.board_size), target_locator_corners, target_locator_found)

        # objp = numpy.zeros((6*7,3), numpy.float32)
        # objp[:,:2] = numpy.mgrid[0:7,0:6].T.reshape(-1,2)
        # print objp

        target_locator_corners = numpy.float32(tuple(_[0] for _ in target_locator_corners))

        # 根据内部角点，对图像进行变换，将棋盘（即locator）还原
        self.logger.debug('warp perspective locator')
        locator_warp_matrix, _ = cv2.findHomography(target_locator_corners, numpy.float32(self.locator_corners))
        self.logger.debug('warp matrix:\n%s', locator_warp_matrix)
        locator = cv2.warpPerspective(target_frame, locator_warp_matrix, tuple(self.src_locator_shape))

        if Debug.is_debug and Debug.frame_show:
            self.imshow('locator', locator)

        # 各种原因导致内部角点的排序可能是错误的
        # 所以变换可能也是错误的
        # 需要寻找方向标记来判断是否错误

        # 将棋盘总体做一次二值化
        locator_threshold, locator_bin = self.threshold(cv2.cvtColor(locator, cv2.COLOR_BGR2GRAY))
        self.logger.debug('threshold chessboard with threshold: %f', locator_threshold)
        # 获取各个可能是方向标记的单元格
        locator_vertex_markers = [locator_bin[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
                                  for rect in self.locator_vertex_rects]
        self.logger.debug('find direction marker')
        marker_index = self.find_direction_marker(locator_vertex_markers)

        if marker_index < 0:
            # 找不到方向标记
            self.logger.warning('can not find direction marker')
            return self.INVALID_RESULT

        self.logger.debug('direction marker found, marker_index is %d', marker_index)

        if Debug.is_debug:
            direction_marker = locator_vertex_markers[marker_index]

            if Debug.frame_show:
                self.imshow('marker', direction_marker)

        self.logger.debug('find white edge by direction marker')
        white_edge_index = self.find_white_edge(locator_vertex_markers[marker_index])
        self.logger.debug('white_edge_index is %d', white_edge_index)

        if white_edge_index < 0:
            self.logger.warning('can not find white edge')
            return self.INVALID_RESULT

        # 修正内部角点的顶点排序
        self.logger.debug('fix order of locator corners')
        ordered_locator_corners = self.fix_locator_corners_order(target_locator_corners,
                                                                   marker_index, white_edge_index)

        if not ordered_locator_corners:
            self.logger.warning('can not fix locator corners order')
            return self.INVALID_RESULT

        self.logger.debug('locator vertexes is fixed')
        if self.logger.isEnabledFor(logging.DEBUG):
            for i in range(len(ordered_locator_corners)):
                self.logger.debug('locator vertex %d %s', i, tuple(ordered_locator_corners[i]))

        ordered_locator_vertexes = numpy.float32(tuple(ordered_locator_corners[i] for i in self.locator_vertex_indexes))

        # 修正后，将棋盘（即locator）和进度条（即progressor）还原
        self.logger.debug('warp perspective locator and progressor')
        src_locator_vertexes = numpy.float32(tuple(self.locator_corners[i] for i in self.locator_vertex_indexes))
        fixed_locator_warp_matrix = cv2.getPerspectiveTransform(numpy.float32(ordered_locator_vertexes), src_locator_vertexes)
        self.logger.debug('warp matrix:\n%s', fixed_locator_warp_matrix)
        fixed_roi = cv2.warpPerspective(target_frame, fixed_locator_warp_matrix, tuple(self.roi_shape))

        if Debug.is_debug and Debug.frame_show:
            self.imshow('fixed roi', fixed_roi)

        # 截取进度条（即progressor）
        progressor = fixed_roi[0:self.progressor_shape[1], self.src_locator_shape[0]:self.src_locator_shape[0] + self.progressor_shape[0]]

        # 进度条（即progressor）可能有少许变形，需要修正
        # 先找到4个顶点
        self.logger.debug('warp perspective progressor by 4-vertexes')
        self.logger.debug('find progressor 4-vertexes')
        # marker与progressor比较接近, 使用相同的阀值去二值化
        if not self.has_progressor(progressor, locator_threshold):
            self.logger.warning('there is no progressor')
            return self.INVALID_RESULT

        target_progressor_vertexes = self.find_progressor_vertexes(progressor, locator_threshold)
        if target_progressor_vertexes is not None:
            self.logger.debug('progressor 4-vertexes found')
            if self.logger.isEnabledFor(logging.DEBUG):
                for i in range(len(target_progressor_vertexes)):
                    self.logger.debug('progressor vertex %d %s', i, tuple(target_progressor_vertexes[i]))

            # 再做一次还原
            self.logger.debug('warp perspective progressor after fixed')
            fixed_progressor_warp_matrix = cv2.getPerspectiveTransform(numpy.float32(target_progressor_vertexes),
                                                                       self.progressor_vertexes)
            self.logger.debug('warp matrix:\n%s', fixed_progressor_warp_matrix)
            fixed_progressor = cv2.warpPerspective(progressor, fixed_progressor_warp_matrix,
                                                   tuple(self.progressor_shape))
        else:
            self.logger.warning('can not find progressor 4-vertexes, ignore fixing')
            fixed_progressor = progressor

        if Debug.is_debug and Debug.frame_show:
            self.imshow('fixed progressor', fixed_progressor)

        # 二值化
        self.logger.debug('parse progress')
        fixed_gray_progressor = cv2.cvtColor(fixed_progressor, cv2.COLOR_BGR2GRAY)
        # _, fixed_binary_progressor = cv2.threshold(fixed_gray_progressor, locator_threshold, 255, cv2.THRESH_BINARY)
        # from matplotlib import pyplot as plt
        # plt.hist(fixed_gray_progressor.ravel(), 256)
        # plt.show()
        _, fixed_binary_progressor = cv2.threshold(fixed_gray_progressor, locator_threshold, 255, cv2.THRESH_OTSU)


        # 利用每个cell的中点进行判断, 生产进度矩阵
        progressor_matrix = self.get_progressor_matrix(fixed_binary_progressor)
        self.logger.debug('progress matrix:\n%s', progressor_matrix)

        # 每行各自求和, 计算出每行的列进度
        row_whitecounts = numpy.sum(progressor_matrix, axis=1).astype('uint8')

        # TODO 这里有些情况可能是二值化阀值过高导致的，之后再考虑如何处理
        if row_whitecounts[self.progress_size[1] - 1] > 0 and row_whitecounts[0] > 0:
            # 第一行和最后一行都有白色, 说明跨越了
            # 这个时候的行进度应该是，最小黑行的前一行
            progress_white_rows = numpy.where(row_whitecounts == 0)
            progress_white_row = numpy.min(progress_white_rows) - 1 if len(progress_white_rows) > 0 else -1
        else:
            # 否则, 行进度就是最大白行
            progress_white_rows = numpy.where(row_whitecounts > 0)
            progress_white_row = numpy.max(progress_white_rows) if len(progress_white_rows) > 0 else -1

        progress_white_col = row_whitecounts[progress_white_row] - 1 if progress_white_row >= 0 else -1

        self.logger.debug('progress row is %d, col is %d', progress_white_row, progress_white_col)

        if Debug.is_debug:
            debug_progressor = cv2.copyMakeBorder(fixed_progressor, self.write_border_size, self.write_border_size, self.write_border_size,
                                                  self.write_border_size, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            # self.imshow('binary progressor', binary_progressor)
            debug_binary_progressor = cv2.copyMakeBorder(cv2.cvtColor(fixed_binary_progressor, cv2.COLOR_GRAY2BGR), 
                                                         self.write_border_size, self.write_border_size, self.write_border_size, 
                                                         self.write_border_size, cv2.BORDER_CONSTANT, value=(255, 255, 255))

            for debug_progressor_image in (debug_progressor, debug_binary_progressor):
                y = self.write_border_size
                cv2.line(debug_progressor_image, (0, y), (debug_progressor_image.shape[1], y), (0, 0, 255), thickness=1)
                for j in range(self.progress_size[1] + 1):
                    y = self.write_border_size + self.border_size[1] + j * self.cell_shape[1]
                    cv2.line(debug_progressor_image, (0, y), (debug_progressor_image.shape[1], y), (255, 0, 0), thickness=1)
                y = self.write_border_size + self.border_size[1] * 2 + j * self.cell_shape[1]
                cv2.line(debug_progressor_image, (0, y), (debug_progressor_image.shape[1], y), (0, 0, 255), thickness=1)

                x = self.write_border_size
                cv2.line(debug_progressor_image, (x, 0), (x, debug_progressor_image.shape[0]), (0, 0, 255), thickness=1)
                for i in range(self.progress_size[0] + 1):
                    x = self.write_border_size + self.border_size[0] + i * self.cell_shape[0]
                    cv2.line(debug_progressor_image, (x, 0), (x, debug_progressor_image.shape[0]), (255, 0, 0), thickness=1)
                x = self.write_border_size + self.border_size[0] * 2 + self.progress_size[0] * self.cell_shape[0]
                cv2.line(debug_progressor_image, (x, 0), (x, debug_progressor_image.shape[0]), (0, 0, 255), thickness=1)

        if Debug.is_debug and Debug.frame_show:
            self.imshow('progressor with lines', debug_progressor)
            self.imshow('binary progressor with lines', debug_binary_progressor)

        return progress_white_row, progress_white_col


class ProgressResultWriter(object):
    def __init__(self, path):
        self.path = path
        self.file = None
        self.writer = None

    def __enter__(self):
        if not Debug.is_debug:
            self.file = open(self.path, 'wb')
            self.writer = csv.writer(self.file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file is not None:
            self.file.close()

            self.writer = None
            self.file = None

    def writerow(self, *args, **kwargs):
        if Debug.is_debug:
            logging.debug(args[0])
        elif self.writer is not None:
            self.writer.writerow(*args, **kwargs)


class FramesProgressDetector(object):
    def __init__(self, progress_detector, frame_filepaths, progress_csv_path, starttime=None):
        self.progress_detector = progress_detector
        self.frame_filepaths = frame_filepaths
        self.progress_csv_path = progress_csv_path
        self.starttime = datetime.datetime.now() if starttime is None else starttime

    def detect(self):
        with ProgressResultWriter(self.progress_csv_path) as progress_writer:
            progress_writer.writerow(['timestamp', 'frame_name', 'progress', 'row', 'col'])

            counter = 0
            for frame_filepath in self.frame_filepaths:
                frame_name = os.path.splitext(os.path.basename(frame_filepath))[0]
                frame = cv2.imread(frame_filepath)
                row, col = self.progress_detector.detect(frame, frame_name=frame_name)
                if row < 0 or col < 0:
                    progress = -1
                else:
                    progress = row * self.progress_detector.progress_size[0] + col

                frame_endtime = datetime.datetime.now()
                frame_timedelta = frame_endtime - self.starttime

                frame_timestamp = timedelta_milliseconds(frame_timedelta)
                progress_writer.writerow([frame_timestamp, frame_name, progress, row, col])

                counter += 1
                if counter % 100 == 0:
                    logging.info('detected %d frames', counter)

            logging.info('detected %d frames', counter)


class FluencyCalculator(object):
    def __init__(self, video_name, progress_csv_path, frame_rate, result_csv_path, start_second=None, end_second=None):
        self.video_name = video_name
        self.progress_csv_path = progress_csv_path
        self.frame_rate = frame_rate
        self.result_csv_path = result_csv_path

        self.start_second = start_second
        self.end_second = end_second

    def process(self):
        if Debug.is_debug:
            return
        valid_frame_counts = {}
        with open(self.progress_csv_path, 'rb') as progress_csv_file:
            csv_reader = csv.reader(progress_csv_file)
            next(csv_reader, None)  # ignore header

            start_frame_num = None

            prev_second = None
            prev_progress = None
            for csv_row in csv_reader:
                frame_timestamp, current_frame_name, current_progress, progress_row, progress_col = csv_row
                # current_frame_num = int(current_frame_name[-5:])
                current_frame_num = int(current_frame_name[len(self.video_name):])

                if start_frame_num is None:
                    start_frame_num = current_frame_num
                    current_second = 1
                    valid_frame_counts['1'] = 1
                else:
                    current_second = int(math.floor((current_frame_num - start_frame_num) / self.frame_rate)) + 1
                    if current_second != prev_second:
                        # next second
                        if current_progress != prev_progress:
                            valid_frame_counts[str(current_second)] = 1
                        else:
                            valid_frame_counts[str(current_second)] = 0
                    else:
                        # same second
                        if current_progress != prev_progress:
                            valid_frame_counts[str(current_second)] += 1

                prev_second = current_second
                prev_progress = current_progress

        max_second = 0
        for second in valid_frame_counts.keys():
            second = int(second)
            max_second = second if second > max_second else max_second


        start_second = self.start_second if self.start_second else 1
        end_second = self.end_second if self.end_second else max_second
        counts = [
            valid_frame_counts[str(second)] if str(second) in valid_frame_counts else 0 for second in range(start_second, end_second)
        ]
        avg_count = sum(counts) / float(len(counts))

        with open(self.result_csv_path, 'wb') as result_csv_path:
            csv_writer = csv.writer(result_csv_path)

            for second in range(1, max_second + 1):
                count = valid_frame_counts[str(second)] if str(second) in valid_frame_counts else 0
                csv_writer.writerow([second, count])

            csv_writer.writerow(['-', avg_count])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='logging verbose')
    # debug
    Debug.add_arguments(parser)

    # extract
    parser.add_argument('-r', '--frame-rate', type=float, default=60.0, help='frame rate')
    parser.add_argument('-t', '--frame-type', default='jpg', help='frame type')

    # detect
    parser.add_argument('-bt', '--binary-threshold', type=int, help='binary threshold')

    # calc
    parser.add_argument('-ss', '--start-second', type=int, default=10, help='start second')
    parser.add_argument('-es', '--end-second', type=int, default=121, help='end second')

    # steps
    parser.add_argument('--just-extract', action='store_true', default=False, help='just extract frames')
    parser.add_argument('--just-detect', action='store_true', default=False, help='just detect frames')
    parser.add_argument('--just-calc', action='store_true', default=False, help='just calculate')

    parser.add_argument('-ob', '--output-base', help='output base dir')
    parser.add_argument('videos_or_frame_dirs', nargs='+')
    args = parser.parse_args()

    logging_config = {
        'level': logging.INFO,
        'stream': sys.stdout,
        'format': '%(asctime)s [%(levelname)s] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }
    if args.verbose:
        logging_config['level'] = logging.DEBUG

    logging.basicConfig(**logging_config)

    # debug
    Debug.parse(args)

    frame_rate = args.frame_rate
    frame_type = args.frame_type

    # steps
    just_flags = (just_extract, just_detect, just_calc, ) = (args.just_extract, args.just_detect, args.just_calc, )
    assert sum(1 for _ in just_flags if _) <= 1

    all_do = not any(just_flags)
    do_flags = [_ or all_do for _ in just_flags]

    do_extract, do_detect, do_calc = do_flags

    output_base = args.output_base

    # options
    src_frame_shape = numpy.array((1080, 1920))

    board_size = numpy.array((4, 4))
    progress_size = numpy.array((10, 5))

    cell_shape = numpy.array((50, 50))
    border_size = numpy.array((20, 20))
    marker_size = 20  # 30

    write_border_size = 20

    # init
    progress_detector = ProgressDetector(src_frame_shape,
                                         board_size, progress_size, cell_shape, border_size, marker_size,
                                         binary_threshold=args.binary_threshold,
                                         write_border_size=write_border_size)

    if Debug.is_debug:
        if len(args.videos_or_frame_dirs) > 1:
            logging.warn('debug mode is turn on, only the first path is available')
        videos_or_frame_dirs = args.videos_or_frame_dirs[:1]
    else:
        videos_or_frame_dirs = args.videos_or_frame_dirs

    for video_or_frame_dir in videos_or_frame_dirs:
        video_starttime = datetime.datetime.now()

        video_or_frame_dir = os.path.abspath(video_or_frame_dir)

        output_base_dir = os.path.dirname(video_or_frame_dir) if output_base is None else output_base
        frame_extractor = FrameExtractor(video_or_frame_dir, frame_rate,
                                         output_base_dir=output_base_dir, frame_type=frame_type)

        logging.info('fluency detection start, %s %s', frame_extractor.type, frame_extractor.path)

        try:
            if do_extract:
                logging.info('extract frames, %s', frame_extractor.path)
                frame_extractor.extract()

            if Debug.is_debug:
                frame_filepaths = frame_extractor.get_frame_filepath_by_num(Debug.frame_num)
            else:
                frame_filepaths = frame_extractor.get_frame_filepaths()

            progress_csv_path = os.path.join(output_base_dir, frame_extractor.video_name + '_progress.csv')
            frames_progress_detector = FramesProgressDetector(progress_detector, frame_filepaths, progress_csv_path,
                                                              starttime=video_starttime)
            if do_detect:
                logging.info('detect progress, %s', frame_extractor.frame_dir)
                logging.info('write progress to %s', progress_csv_path)
                frames_progress_detector.detect()

            if do_calc:
                logging.info('calculate fluency, %s', frame_extractor.frame_dir)
                result_csv_path = os.path.join(output_base_dir, frame_extractor.video_name + '_result.csv')
                logging.info('write fluency to %s', result_csv_path)
                fluency_calculator = FluencyCalculator(frame_extractor.video_name, frames_progress_detector.progress_csv_path,
                                                       frame_rate, result_csv_path,
                                                       start_second=args.start_second,
                                                       end_second=args.end_second)
                fluency_calculator.process()
        except Exception:
            logging.exception('fluency detection error, %s %s', frame_extractor.type, frame_extractor.path)

        video_endtime = datetime.datetime.now()
        video_timedelta = video_endtime - video_starttime
        video_time_splits = str(video_timedelta).split(':')
        video_time_str = '%s hours %s minutes %s seconds' % \
                         (video_time_splits[0], video_time_splits[1], video_time_splits[2])

        logging.info('fluency detection end, %s %s',
                     frame_extractor.type, frame_extractor.path)
        logging.info('total used %d milliseconds (%s)',
                     timedelta_milliseconds(video_timedelta), video_time_str)

if __name__ == '__main__':
    main()