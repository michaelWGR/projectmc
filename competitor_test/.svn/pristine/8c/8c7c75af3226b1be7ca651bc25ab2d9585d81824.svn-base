# -*- coding:utf-8 -*-

import argparse
import os
import cv2
import csv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def binary_image(threshold, imagePath, outputPath):
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
    return black_detector

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

def find_upBound(black_detectors, diffs, maxgray, mingray):
    maxDiff_index = diffs.index(max(diffs[0: len(diffs)/2]))
    if black_detectors[maxDiff_index][1]>maxgray and black_detectors[maxDiff_index+1][1]<mingray:
        return maxDiff_index
    else:
        return -1

def find_lowBound(black_detectors, diffs, maxgray, mingray):
    minDiff_index = diffs.index(min(diffs[len(diffs)/2: len(diffs)]))
    if black_detectors[minDiff_index][1]<mingray and black_detectors[minDiff_index+1][1]>maxgray:
        return minDiff_index
    else:
        return len(black_detectors)

def write_grag(black_detectors, result_csv_path):
    with open(result_csv_path, 'wb') as result_csv_path:
        csv_writer = csv.writer(result_csv_path)
        for (sourcepath, black_detector) in black_detectors:
            csv_writer.writerow((sourcepath, black_detector))
        return None

def delete_grayframes(black_detectors, maxDiff_index, minDiff_index):
    if maxDiff_index != -1:
        for j in range(0, maxDiff_index+1):
            if os.path.exists(black_detectors[j][0]):
                os.remove(black_detectors[j][0])
    if minDiff_index != len(black_detectors):
        for k in range(len(black_detectors)-1, minDiff_index, -1):
            if os.path.exists(black_detectors[k][0]):
                os.remove(black_detectors[k][0])
    return None

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

        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)

        # 计算每张图的平均灰度值
        black_detectors = []
        for file in os.listdir(videoPath):
            if file.endswith('.bmp') or file.endswith('.BMP'):
                if os.listdir(videoPath).index(file)%500 == 0:
                    print 'processing {0} {1} frames, please wait......(total:{2})'.format(videoBasename, os.listdir(videoPath).index(file), len(os.listdir(videoPath)))
                filePath = os.path.join(videoPath, file)
                outputPath = os.path.join(outputDir, file)
                black_detector = float(binary_image(threshold, filePath, outputPath))
                black_detectors.append((filePath, black_detector))
        if os.path.isdir(outputDir):
            os.rmdir(outputDir)
        write_grag(black_detectors, result_csv_path)
        # 计算前后两张图的灰度差分
        diffs = calcDiff(black_detectors)
        # 寻找灰度上边界
        maxDiff_index = find_upBound(black_detectors, diffs, maxgray, mingray)
        # 寻找灰度下边界
        minDiff_index = find_lowBound(black_detectors, diffs, maxgray, mingray)
        # 删除上边界之前和下边界之后的帧
        delete_grayframes(black_detectors, maxDiff_index, minDiff_index)

if __name__ == "__main__":
    main()
