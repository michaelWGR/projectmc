# -*- coding:utf-8 -*-

import os
import sys
import datetime
import cv2
import math
import numpy
import argparse
import csv

import logging


#6.5025, 58.5225
def ssim(img1, img2, C=(6.5025, 58.5225), window=(11, 11, 1.5)):
    C1 = C[0]
    C2 = C[1]
    i1 = img1.astype(float)
    i2 = img2.astype(float)
    
    i1_2 = i1 * i1 # i1^2
    i2_2 = i2 * i2 # i2^2
    i1_i2 = i1 * i2 # i1 * i2
    
    mu1 = cv2.GaussianBlur(i1, window[0:2], window[2]) 
    mu2 = cv2.GaussianBlur(i2, window[0:2], window[2])
    
    mu1_2 = mu1 * mu1
    mu2_2 = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    
    sigma1_2 = cv2.GaussianBlur(i1_2, window[0:2], window[2])
    sigma1_2 = sigma1_2 - mu1_2
    
    sigma2_2 = cv2.GaussianBlur(i2_2, window[0:2], window[2])
    sigma2_2 = sigma2_2 - mu2_2
    
    sigma12 = cv2.GaussianBlur(i1_i2, window[0:2], window[2])
    sigma12 = sigma12 - mu1_mu2
    
    t1 = 2 * mu1_mu2 + C1
    t2 = 2 * sigma12 + C2
    t3 = t1 * t2 # t3 = ((2*mu1_mu2 + C1).*(2*sigma12 + C2))
    
    t1 = mu1_2 + mu2_2 + C1;
    t2 = sigma1_2 + sigma2_2 + C2;
    t1 = t1 * t2 # t1 =((mu1_2 + mu2_2 + C1).*(sigma1_2 + sigma2_2 + C2))
    
    ssim_map = t3 / t1 # ssim_map =  t3./t1
    
    ssim_scalar = cv2.mean(ssim_map)
    return ssim_scalar[0]


valid_exts = [ '.bmp' ]


class MipMapResolver(object):
    def __init__(self):
        super(MipMapResolver, self).__init__()
    
    def imread(self, frame, level, *args, **kwargs):
        pass

    def imread_all(self, frame, level, *args, **kwargs):
        pass


class MemMipMapResolver(MipMapResolver):
    def __init__(self):
        super(MemMipMapResolver, self).__init__()
    
    def imread(self, frame, level, *args, **kwargs):
        frame_image = frame.imread(*args, **kwargs)
        while level > 0:
            frame_image = cv2.pyrDown(frame_image)
            level -= 1
        return frame_image

    def imread_all(self, frame, level, *args, **kwargs):
        frame_images = []
        
        frame_image = frame.imread(*args, **kwargs)
        frame_images.append(frame_image)
        for i in range(1, level + 1):
            frame_image = cv2.pyrDown(frame_image)
            frame_images.append(frame_image)
            level -= 1
        return frame_images


class LocalMipMapResolver(MipMapResolver):
    def __init__(self):
        super(LocalMipMapResolver, self).__init__()
    
    def imread(self, frame, level, *args, **kwargs):
        if level <=0:
            return frame.imread(*args, **kwargs)
        frame_dir = os.path.dirname(frame.path)
        mip_map_image_path = os.path.join(frame_dir, 'mip_map', str(level), frame.filename)
        return cv2.imread(mip_map_image_path, *args, **kwargs)
    
    def imread_all(self, frame, level, *args, **kwargs):
        frame_images = []
        
        for i in range(0, level + 1):
            frame_image = self.imread(frame, i, *args, **kwargs)
            frame_images.append(frame_image)
            level -= 1
        return frame_images


class Frame(object):
    def __init__(self, frame_path):
        super(Frame, self).__init__()
        frame_path = os.path.abspath(frame_path)
        if not os.path.isfile(frame_path):
            raise ValueError('frame %s is not file' % (frame_path, ))
        self.path = frame_path
        self.filename = os.path.basename(frame_path)
        self.name = os.path.splitext(self.filename)[0]
        self.ext = os.path.splitext(self.filename)[1]
        self.num = int(self.name[-5:])
    
    def imread(self, *args, **kwargs):
        return cv2.imread(self.path, *args, **kwargs)


def list_frames_by_path(frames_dir, include=None):
    if include is None:
        include_paths = [
                            os.path.join(frames_dir, filename) for filename in os.listdir(frames_dir) 
                            if os.path.splitext(filename)[1] in valid_exts
                        ]
    else:
        include_paths = [
                           (include_item if os.path.isabs(include_item) else os.path.join(frames_dir, include_item))
                           for include_item in include
                        ]

    frames = [Frame(file_path) for file_path in include_paths]
    # 因为某些文件系统可能不会按照字母顺序排序, 所以按照帧号进行排序
    frames.sort(key=lambda frame: frame.num)
    return frames


class Frames(object):
    def __init__(self, frames_dir, include=None):
        super(Frames, self).__init__()
        self.frames_dir = frames_dir
        self.frames = list_frames_by_path(frames_dir, include=include)
        self._num_map = {}
        for i in range(0, len(self.frames)):
            frame = self.frames[i]
            self._num_map[frame.num] = i
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        pass
    
    def __len__(self):
        return len(self.frames)
    
    def get(self, index):
        if index < 0 or index >= len(self.frames):
            return None
        return self.frames[index]
    
    def get_index_by_num(self, num):
        index = None
        if num in self._num_map:
            index = self._num_map[num]
        return index
    
    def get_by_num(self, num):
        index = self.get_index_by_num(num)
        return self.get(index) if index is not None else None


class FrameFilter(object):
    def __init__(self):
        super(FrameFilter, self).__init__()
    
    def filter(self, frame, *args, **kwargs):
        pass


class NothingFrameFilter(FrameFilter):
    def __init__(self):
        super(NothingFrameFilter, self).__init__()
    
    def filter(self, frame, *args, **kwargs):
        return frame.imread(*args, **kwargs)


class ROIFrameFilter(FrameFilter):
    def __init__(self, x=0, y=0, width=0, height=0):
        super(ROIFrameFilter, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def filter(self, frame, *args, **kwargs):
        frame_image = frame.imread(*args, **kwargs)
        return frame_image[self.y:self.y+self.height, self.x:self.x+self.width]


class RangedFrames(object):
    def __init__(self, frames, start, end):
        super(RangedFrames, self).__init__()
        self.frames = frames
        self.start = start
        self.end = end
    
    def __getitem__(self, index):
        return self.get(index)
    
    def __setitem__(self, index, value):
        pass
    
    def __len__(self):
        return self.end - self.start
    
    def get(self, index):
        if index < self.start or index >= self.end:
            return None
        return self.frames[index]
    
    def get_index_by_num(self, num):
        index = self.frames.get_index_by_num(num)
        return index if index < self.start or index >= self.end else None
    
    def get_by_num(self, num):
        index = self.get_index_by_num(num)
        return self.get(index) if index is not None else None


class FramesAlign(object):
    def __init__(self, src_frames, target_frames, level=4, frame_filter=None):
        super(FramesAlign, self).__init__()
        self.src_frames = src_frames
        self.src_mip_map_resolver = LocalMipMapResolver()
        self.target_frames = target_frames
        self.target_mip_map_resolver = MemMipMapResolver()
        self.level = level
        self.frame_filter = frame_filter if frame_filter is not None else NothingFrameFilter()
        
        self.finished = False
        self.results = None
    
    def _find_max_ssim_by_level(self, cur_level, src_indexes, target_index, target_mip_map):
        first = True
        max_src_indexes = []
        max_ssim = 0
        for i in src_indexes:
            src_frame = self.src_frames[i]
            
            src_img = self.src_mip_map_resolver.imread(src_frame, cur_level, cv2.IMREAD_GRAYSCALE)
            
            ssim_val = ssim(src_img, target_mip_map[cur_level])
            # logging.debug('ssim(%s, %s) = %f', src_path[cur_level], target_path, ssim_val)
            
            ssim_diff = ssim_val - max_ssim
            if not first and abs(ssim_diff) >= 1e-7 and ssim_diff < 0:
                continue
            
            if first or abs(ssim_diff) >= 1e-7:
                # logging.debug('change max ssim %f, max src index %d', ssim_val, i)
                max_ssim = ssim_val
                max_src_indexes = [i]
            else:
                # logging.debug('append max src index %d', i)
                if ssim_diff > 0:
                    max_src_indexes.insert(0, i)
                else:
                    max_src_indexes.append(i)
            first = False
        return max_ssim, max_src_indexes
    
    class AlignResult(object):
        def __init__(self, src_index, target_index, ssim_val):
            super(FramesAlign.AlignResult, self).__init__()
            self.src_index = src_index
            self.target_index = target_index
            self.ssim_val = ssim_val
    
    def find_max_ssim(self, src_range, target_index):
        target_frame = self.target_frames[target_index]
        target_mip_map = self.target_mip_map_resolver.imread_all(target_frame, self.level, cv2.IMREAD_GRAYSCALE)
        
        max_ssim = 0.0
        max_src_indexes = range(src_range[0], src_range[1])
        for cur_level in range(self.level,-1,-1):
            max_ssim, max_src_indexes = self._find_max_ssim_by_level(cur_level, max_src_indexes, target_index, target_mip_map)
            if len(max_src_indexes) == 1:
                return FramesAlign.AlignResult(max_src_indexes[0], target_index, max_ssim)
            logging.info('%s level = %d has too many similar frams (count=%d), use lower level', target_frame.filename, cur_level, len(max_src_indexes))
        return FramesAlign.AlignResult(max_src_indexes[0], target_index, max_ssim)
    
    def _src_format(self, index):
        return '%d' % (self.src_frames[index].num, )
    
    def _src_range_format(self, index_range):
        return '%s, %s' % (self._src_format(index_range[0]), self._src_format(index_range[1] - 1))
    
    def _target_format(self, index):
        return '%d' % (self.target_frames[index].num, )
    
    def _target_range_format(self, index_range):
        return '%s, %s' % (self._target_format(index_range[0]), self._target_format(index_range[1] - 1))
    
    def _find_max_ssim_with_depth(self, src_range, target_index, depth=0):
        logging.debug('[depth: %d] find_max_ssim src[%s], target[%s]', depth, self._src_range_format(src_range), self._target_format(target_index))
        result = self.find_max_ssim(src_range, target_index)
        logging.debug('[depth: %d] found max_ssim src[%s], target[%s]', depth, self._src_format(result.src_index), self._target_format(target_index))
        return result
    
    def _align_frames(self, src_range, target_range, depth=0):
        logging.debug('[depth: %d] align_frames src[%s], target[%s]', depth, self._src_range_format(src_range), self._target_range_format(target_range))
        if target_range[0] >= target_range[1]:
            # target_range is empty
            logging.debug('[depth: %d] target_range is empty, just return', depth)
            return []

        if src_range[0] >= src_range[1]:
            # src_range is empty
            logging.debug('[depth: %d] src_range is empty', depth)
            # however, we caculate ssim
            logging.debug('[depth: %d] just caculate ssim', depth)
            logging.debug('[depth: %d] ssim src[%s], target[%s]', depth, self._src_format(src_range[1]), self._target_range_format(target_range))
            results = []
            src_path = self.src_frames[src_range[1]].path
            src_img = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
            for target_index in range(target_range[0], target_range[1]):
                target_img = cv2.imread(self.target_frames[target_index].path, cv2.IMREAD_GRAYSCALE)
                ssim_val = ssim(src_img, target_img)
                results.append(FramesAlign.AlignResult(src_range[1], target_index, ssim_val))
            return results

        target_len = target_range[1] - target_range[0]
        if target_len == 1:
            logging.debug('[depth: %d] only one find_max_ssim', depth)
            results = [self.find_max_ssim(src_range, target_range[0])]
            return results

        results = []
        
        target_mid = (target_range[0] + target_range[1]) / 2
        logging.debug('[depth: %d] split target range target[%s]', depth, self._target_range_format(target_range))
        
        left_target_range = (target_range[0], target_mid)
        logging.debug('[depth: %d] left target range target[%s]', depth, self._target_range_format(left_target_range))
        
        right_target_range = (target_mid, target_range[1])
        logging.debug('[depth: %d] right target range target[%s]', depth, self._target_range_format(right_target_range))
        
        # left range
        src_left_result = self._find_max_ssim_with_depth(src_range, left_target_range[0], depth)
        results.append(src_left_result)

        if left_target_range[0] < left_target_range[1] - 1:
            src_left_mid_result = self._find_max_ssim_with_depth(src_range, left_target_range[1] - 1, depth)
            results.append(src_left_mid_result)

        # right range
        if right_target_range[0] < right_target_range[1] - 1:
            src_right_mid_result = self._find_max_ssim_with_depth(src_range, right_target_range[0], depth)
            results.append(src_right_mid_result)

        src_right_result = self._find_max_ssim_with_depth(src_range, right_target_range[1] - 1, depth)
        results.append(src_right_result)

        if left_target_range[0] < left_target_range[1] - 1:
            left_src_range = (src_left_result.src_index, src_left_mid_result.src_index + 1)
            logging.debug('[depth: %d] left src range src[%s]', depth, self._src_range_format(left_src_range))
        
        if right_target_range[0] < right_target_range[1] - 1:
            right_src_range = (src_right_mid_result.src_index, src_right_result.src_index + 1)
            logging.debug('[depth: %d] right src range src[%s]', depth, self._src_range_format(right_src_range))
        
        # left range
        if left_target_range[0] < left_target_range[1] - 1:
            left_results = self._align_frames(left_src_range, (left_target_range[0] + 1, left_target_range[1] - 1), depth + 1);
            results = results + left_results
        
        # right range
        if right_target_range[0] < right_target_range[1] - 1:
            right_results = self._align_frames(right_src_range, (right_target_range[0] + 1, right_target_range[1] - 1), depth + 1);
            results = results + right_results
        return results

    def align_frames(self):
        if self.finished:
            return
        src_range = (0, len(self.src_frames))
        target_range = (0, len(self.target_frames))
        results = self._align_frames(src_range, target_range, 0)
        results = sorted(results, key=lambda x: x.target_index)
        self.results = results
        self.finished = True
    
    def write_to(self, file_path):
        if not self.finished:
            self.align_frames()
        
        with open(file_path, 'wb') as f:
            writer = csv.writer(f)
            for result in self.results:
                row = [self.target_frames[result.target_index].path, self.src_frames[result.src_index].path, result.ssim_val]
                writer.writerow(row)


def timedelta_milliseconds(timedelta):
    return (timedelta.microseconds + (timedelta.seconds + timedelta.days * 24 * 3600) * 10**6) / 10**3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='width')
    parser.add_argument('--target-x', type=int, dest='target_x', default=0, help='target x')
    parser.add_argument('--target-y', type=int, dest='target_y', default=0, help='target y')
    parser.add_argument('--target-width', type=int, dest='target_width', help='target width')
    parser.add_argument('--target-height', type=int, dest='target_height', help='target height')
    parser.add_argument('--target-include')
    parser.add_argument('--level', type=int, help='mip map level', default=3)
    parser.add_argument('--output-file', help='output file')
    parser.add_argument('src_dir')
    parser.add_argument('target_dir')
    args = parser.parse_args()

    # logging_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging_format = '%(asctime)s [%(levelname)s] %(message)s'
    logging_datefmt = '%Y-%m-%d %H:%M:%S'
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=logging_format, datefmt=logging_datefmt)
    else:
        logging.basicConfig(level=logging.INFO, format=logging_format, datefmt=logging_datefmt)

    target_x = args.target_x
    target_y = args.target_y
    target_width = args.target_width
    target_height = args.target_height
    level = args.level

    src_dir = os.path.abspath(args.src_dir)
    target_dir = os.path.abspath(args.target_dir)
    output_file = args.output_file
    if output_file is None:
        output_file = os.path.join(os.path.dirname(target_dir), os.path.basename(target_dir) + '.csv')

    src_frames = Frames(src_dir)

    target_include_list = None
    if args.target_include:
        target_include_list = []
        target_include_path = os.path.abspath(args.target_include)
        with open(target_include_path, 'rb') as include_file:
            include_reader = csv.reader(include_file)
            for row in include_reader:
                target_include_list.append(row[0])

    target_frames = Frames(target_dir, include=target_include_list)

    target_filter = None
    if target_width is not None and target_height is not None:
        target_filter = ROIFrameFilter(target_x, target_y, target_width, target_height)
    elif (target_width is None) != (target_height is None):
        logging.warn('--target-width or --target-height is empty, it will be ignored.')
        pass

    logging.info('align frames %s, %s', src_dir, target_dir)
    starttime = datetime.datetime.now()

    frames_align = FramesAlign(src_frames, target_frames, level=level)
    frames_align.align_frames()

    endtime = datetime.datetime.now()
    align_timedelta = endtime - starttime
    run_time_splits = str(align_timedelta).split(':')
    run_time_str = '%s hours %s minutes %s seconds' % (run_time_splits[0], run_time_splits[1], run_time_splits[2])
    logging.info('align frames total use %d milliseconds (%s)', timedelta_milliseconds(align_timedelta), run_time_str)

    logging.info('write result to %s', output_file)
    frames_align.write_to(output_file)


if __name__ == '__main__':
    main()
