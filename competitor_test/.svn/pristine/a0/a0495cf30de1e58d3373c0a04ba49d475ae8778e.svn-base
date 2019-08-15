# -*- coding:utf-8 -*-

import argparse
import os
import cv2
import csv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def binary_image(threshold, imagePath):
    outputPath = 'binary.bmp'
    image = cv2.imread(imagePath)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 图片二值化
    if threshold is None:
        _, binaryImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, binaryImage = cv2.threshold(grayImage, threshold, 255, cv2.THRESH_BINARY)
    cv2.imwrite(outputPath, binaryImage)
    # 计算灰度值
    if os.path.exists(outputPath):
        black_detector = calcgray(binaryImage, outputPath)
        os.remove(outputPath)
    return float(black_detector)

def calcgray(image, imagePath):
    width = image.shape[0]
    height = image.shape[1]
    script = r'python {0} --x 0 --y 0 --width {1} --height {2} {3}'.format(os.path.join(BASE_DIR, 'avg_gray.py'), width, height, imagePath)
    return os.popen(script).read().strip()

def calcDiff(black_detectors):
    diffs = []
    for i in range(0, len(black_detectors)-1):
        diff = black_detectors[i][1] - black_detectors[i+1][1]
        diffs.append(diff)
    return diffs

def delete_grayframes(filelist, maxDiff_index, minDiff_index):
    if maxDiff_index != -1:
        for j in range(0, maxDiff_index+1):
            if os.path.exists(filelist[j]):
                os.remove(filelist[j])
    if minDiff_index != len(filelist):
        for k in range(len(filelist)-1, minDiff_index, -1):
            if os.path.exists(filelist[k]):
                os.remove(filelist[k])
    return None

def upSearch(filelist, maxgray, mingray, threshold):
    low = 0
    height = len(filelist)-1
    while low <= height:
        mid = (low+height)/2
        if mid != height:
            if (binary_image(threshold, filelist[mid]) < mingray) and (binary_image(threshold, filelist[mid+1]) < mingray):
                height = mid - 1
            elif (binary_image(threshold, filelist[mid]) > maxgray) and (binary_image(threshold, filelist[mid+1]) > maxgray):
                low = mid + 1
            elif (binary_image(threshold, filelist[mid])) <mingray and (binary_image(threshold, filelist[mid+1]) > maxgray):
                low = mid + 1
            else:
                return mid
        else:
            return mid
    return -1

def lowSearch(filelist, maxgray, mingray, threshold):
    low = 0
    height = len(filelist)-1
    while low <= height:
        mid = (low+height)/2
        #print filelist[mid]
        if mid != height:
            if (binary_image(threshold, filelist[mid]) < mingray) and (binary_image(threshold, filelist[mid+1]) < mingray):
                low = mid + 1
            elif (binary_image(threshold, filelist[mid]) > maxgray) and (binary_image(threshold, filelist[mid+1]) > maxgray):
                height = mid - 1
            elif (binary_image(threshold, filelist[mid])) > maxgray and (binary_image(threshold, filelist[mid+1]) < mingray):
                height = mid - 1
            else:
                return mid
        else:
            return mid
    return len(filelist)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',default=False, help='verbose')
    parser.add_argument('-th', '--threshold', type = float, help='binary threshold')
    parser.add_argument('-mx', '--maxgray', type = float, help='maxgray threshold')
    parser.add_argument('-mn', '--mingray', type = float, help='mingray threshold')
    parser.add_argument('video_paths', nargs='+')
    args = parser.parse_args()

    threshold = args.threshold if args.threshold is not None else 45
    maxgray = args.maxgray if args.maxgray is not None else 250
    mingray = args.mingray if args.mingray is not None else 180
    videoPaths = args.video_paths

    for videoPath in videoPaths:
        videoPath = os.path.abspath(videoPath)
        videoDir = os.path.dirname(videoPath)
        videoBasename = os.path.basename(videoPath)
        outputDir = os.path.join(videoPath,'tmp')
        result_csv_path = os.path.join(videoDir,videoBasename+'_gray.csv')

        filelist = [os.path.join(videoPath, file) for file in os.listdir(videoPath) if file.endswith('.bmp') or file.endswith('.BMP')]
        #寻找灰帧上边界
        gray_upIndex = upSearch(filelist, maxgray, mingray, threshold)
        #寻找灰帧下边界
        gray_lowIndex = lowSearch(filelist, maxgray, mingray, threshold)

        delete_grayframes(filelist, gray_upIndex, gray_lowIndex)

if __name__ == "__main__":
    main()
