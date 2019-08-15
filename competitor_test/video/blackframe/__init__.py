# -*- coding:utf-8 -*-

from utils import FilterFrameGenerator, \
    NothingFrameFilter

__author__ = 'LibX'


class BlackFrame(object):
    def __init__(self, frame_num, result):
        super(BlackFrame, self).__init__()
        self.frame_num = frame_num
        self.result = result


class BlackFrameDetector(object):
    def __init__(self, frame_generator, black_detector, frame_filter=None):
        super(BlackFrameDetector, self).__init__()
        self.frame_generator = frame_generator
        self.black_detector = black_detector
        self.frame_filter = frame_filter if frame_filter is not None else NothingFrameFilter()

    def detect(self):
        black_results = []

        frame_generator = FilterFrameGenerator(self.frame_generator, [self.frame_filter])

        with frame_generator as frames:
            i = 1
            for frame in frames:
                detect_result = self.black_detector.is_black(frame)
                black_results.append(BlackFrame(i, detect_result))

                i += 1
        return black_results
