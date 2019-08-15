# -*- coding:utf-8 -*-
import subprocess
import time
import os
import argparse
import re

# def get_paramas():
#     pass

def crop_video(video_path, save_video_path):
    cmd_crop = "ffmpeg -i {} -vf crop=1072:2208:4:6 -vcodec h264 -acodec aac {}".format(video_path,
                                                                                              save_video_path).split()
    p_crop = subprocess.Popen(cmd_crop)
    p_crop.communicate()


# def cut_video(filename, time):
#     cmd_cut = "ffmpeg -ss 0:0:00 -t 0:0:{} -i {} -vcodec copy -acodec copy cut_video_{}.mp4".format(time, filename,
#                                                                                                     time).split()
#     p_cut = subprocess.Popen(cmd_cut)
#     p_cut.communicate()
#     return "cut_video_{}.mp4".format(time)

# 获取文件里的sms8的mp4所有文件名
def get_file(files_path):
    crop_case_list = ['start', 'pic', 'upload1','upload2','special','magic','complex']
    if not os.path.exists(files_path):
        raise Exception("{0} is not exist".format(files_path))
    video_for_crop = []
    for root, dirs, files in os.walk(files_path):
        pattern = re.compile(r'(.{4})[^_]*_[^_]*_([^_]*)_.*')
        for videofile in files:
            try:
                phone_name = re.match(pattern,videofile).group(1)
                case_name = re.match(pattern,videofile).group(2)
                if phone_name == 'sms8' and videofile.endswith('.mp4'):
                    if case_name in crop_case_list:
                        video_path = os.path.join(files_path, videofile)
                        video_for_crop.append(video_path)
            except AttributeError:
                continue
        return video_for_crop

# 在文件里创建croppedvideo文件
def makedir_croppedvideo(files_path):
    if not os.path.exists(files_path):
        raise Exception("{0} is not exist".format(files_path))
    video_path = os.path.join(files_path,'croppedvideo')
    isExists = os.path.exists(video_path)
    if not isExists:
        os.mkdir(video_path)
    return video_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    files_path = args.file_path
    croppedvideo_path = makedir_croppedvideo(files_path)
    video_list = get_file(files_path)
    for video_path in video_list:
        pattern = re.compile(r'.*\/(.*\.mp4)')
        video_group = re.match(pattern,video_path)
        video_name = video_group.group(1)
        save_video_path = os.path.join(croppedvideo_path,video_name)
        crop_video(video_path,save_video_path)


if __name__ == "__main__":
    main()
    # files_path = '/Users/yyinc/Documents/guirong/projectmc/cutvideo/testvideo'
    # get_file(files_path)
    # filename = "sms8dyin_android_upload2_01.mp4"
    # filename_10s = cut_video(filename,5)
    # begin = time.time()
    # save_filename = "crop_video_5.mp4"
    # crop_video(filename_10s, save_filename)
    # end = time.time()
    # print "crop duration of 10s video is {}s".format(end - begin)

    # filename_60s = cut_video(filename,"60")
    # begin = time.time()
    # save_filename = "crop_video_60.mp4"
    # crop_video(filename_60s, save_filename)
    # end = time.time()
    # print "crop duration of 30s video is {}s".format(end - begin)
