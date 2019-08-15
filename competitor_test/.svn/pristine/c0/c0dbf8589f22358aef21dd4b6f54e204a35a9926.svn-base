# -*- coding:UTF-8 -*-
import os
import re
import subprocess
import cv2
import cv2.cv as cv
import sys

ffmpeg_default_path = 'C:\\ffmpeg\\bin'
video_frame_paths = []
mobile_threshold = 10.0
game_live_threshold = 0.0
result = []


def show_help():
    print u'''用法：python delay_detect.py -p 视频所在路径 -r 帧率 -t 视频类型(g:游戏直播/m:移动直播) -c 切割参数(x,y,width,height)'''
    print u"示例: python delay_detect.py -p D:\\test -r 60 -t m -c 0,300,1080,300"


def get_params():
    global video_path
    global bit_rate
    global is_mobile
    global size
    count = 1
    while count < len(sys.argv):
        if sys.argv[count] == '-h':
            show_help()
            sys.exit(0)
        if sys.argv[count] == '-p':
            count += 1
            if os.path.isdir(sys.argv[count]):
                video_path = sys.argv[count]
            else:
                print u"参数错误"
                show_help()
                sys.exit(0)
        if sys.argv[count] == '-r':
            count += 1
            if 0 < int(sys.argv[count]) <= 60:
                bit_rate = sys.argv[count]
            else:
                print u"参数错误"
                show_help()
                sys.exit(0)
        if sys.argv[count] == '-t':
            count += 1
            if sys.argv[count] == 'm':
                is_mobile = True
            elif sys.argv[count] == 'g':
                is_mobile = False
            else:
                print u"参数错误"
                show_help()
                sys.exit(0)
        if sys.argv[count] == '-c':
            count += 1
            pattern = re.compile(r'\d*,\d*,\d*,\d*')
            if pattern.match(sys.argv[count]) is not None:
                size = {}
                input_size = str(sys.argv[count]).split(",")
                size['x'] = int(input_size[0])
                size['y'] = int(input_size[1])
                size['width'] = int(input_size[2])
                size['height'] = int(input_size[3])
            else:
                print u"参数错误"
                show_help()
                sys.exit(0)
        count += 1


def extract(arg_video_path, arg_frame_path, arg_video_name, bit_rate, arg_ffmpeg_path=ffmpeg_default_path):
    if os.path.exists(arg_frame_path) == False:
        os.mkdir(arg_frame_path)
    image_file_pattern = os.path.join(arg_frame_path, arg_video_name + "%5d.bmp")
    cmd = [os.path.join(arg_ffmpeg_path, "ffmpeg"), '-i', arg_video_path, '-r', str(bit_rate), '-f', 'image2', image_file_pattern]
    child = subprocess.Popen(cmd)
    child.wait()


def is_image_file(file_name):
    return os.path.splitext(file_name)[1] == '.bmp'


def caculate_gray_value(img):
    sum = 0
    average = 0
    cols = img.shape[1]
    rows = img.shape[0]
    for i in range(rows):  # traverses through height of the image
        for j in range(cols):  # traverses through width of the image
            sum += img[i][j]
    average = sum/(cols*rows)
    print average
    return average


def detect_first_frame_gray(arg_frame_path):
    frames = [os.path.join(arg_frame_path, _) for _ in os.listdir(arg_frame_path) if is_image_file(_)]
    count = 1
    if is_mobile:
        for frame in frames:
            print count
            img = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
            roi_img = img[size['y']:size['y'] + size['height'], size['x']:size['x'] + size['width']]
            resize_img = cv2.resize(roi_img, (0, 0), fx=0.2, fy=0.2)
            if caculate_gray_value(resize_img) > mobile_threshold:
                break
            count += 1
    else:
        for frame in frames:
            img = cv2.imread(frame, cv2.IMREAD_GRAYSCALE)
            roi_img = img[size['y']:size['y'] + size['height'], size['x']:size['x'] + size['width']]
            resize_img = cv2.resize(roi_img, (0, 0), fx=0.2, fy=0.2)
            if caculate_gray_value(resize_img) > game_live_threshold:
                break
            count += 1
    print count
    return count


def delay_detect():
    videos = os.listdir(video_path)
    for video in videos:
        if os.path.splitext(video)[1] in ('.mov', '.mp4', '.avi'):
            video_name = os.path.splitext(video)[0]
            frame_path = os.path.join(video_path, video_name)
            print video + " is extracting."
            # extract(os.path.join(video_path, video), frame_path, video_name, int(bit_rate))
            video_frame_paths.append(frame_path)
    for video_frame_path in video_frame_paths:
        print video_frame_path + " is caculating!"
        result.append(detect_first_frame_gray(video_frame_path))
    if len(result) == 2:
        delay = abs(float(result[0]) - float(result[1])) / float(bit_rate)
    else:
        delay = "Data error"
    print delay


if __name__ == "__main__":
    get_params()
    delay_detect()
