# -*- coding:utf-8 -*-
import cv2
import numpy

__author__ = 'LibX'


class DetectResult(object):
    def __init__(self, is_black, *args, **kwargs):
        super(DetectResult, self).__init__(*args, **kwargs)
        self.is_black = is_black


class Detector(object):
    def __init__(self, *args, **kwargs):
        super(Detector, self).__init__(*args, **kwargs)

    def is_black(self, image):
        raise NotImplementedError()


class AverageGrayDetectResult(DetectResult):
    def __init__(self, is_black, avg_gray, *args, **kwargs):
        super(AverageGrayDetectResult, self).__init__(is_black, *args, **kwargs)
        self.avg_gray = avg_gray


class AverageGrayThresholdDetector(Detector):
    def __init__(self, threshold, *args, **kwargs):
        super(AverageGrayThresholdDetector, self).__init__(*args, **kwargs)
        self.threshold = threshold

        self.ksize = (11, 11)
        self.sigmaX = 1.5

    def get_avg_gray(self, image):
        gray_image = image
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray_image = gray_image.astype(float)
        gray_image = cv2.GaussianBlur(gray_image, self.ksize, self.sigmaX)

        avg_gray = numpy.average(gray_image)
        return avg_gray

    def is_black(self, image):
        avg_gray = self.get_avg_gray(image)
        return AverageGrayDetectResult(avg_gray <= self.threshold, avg_gray)
