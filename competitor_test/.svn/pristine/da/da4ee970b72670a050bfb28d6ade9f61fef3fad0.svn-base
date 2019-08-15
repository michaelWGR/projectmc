# -*- coding:utf-8 -*-


import argparse
import os
import cv2
import numpy 
import csv

class VideoDelayDetector(object):
    def __init__(self, actor_path, viewer_path, div_val):
        self.actor_path = actor_path
        self.viewer_path = viewer_path
        self.div_val = div_val


    def process_detect(self):
        actor_frame = 0
        viewer_frame = 0
        if os.path.exists(self.actor_path):
            last = 0
            for _image in os.listdir(self.actor_path):
                if _image.endswith('.jpg') and not _image.startswith('.'):
                    image_obj = cv2.imread(os.path.join(self.actor_path, _image))
                    gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)
                    avg_gray = numpy.average(gray)
                    if last == 0 :
                        last = avg_gray
                    else:
                        if float(avg_gray) - float(last) > float(self.div_val):
                            actor_frame = _image[-9:-4]
                            break
                    last = avg_gray
        else:
            actor_frame = 0

        if os.path.exists(self.viewer_path):
            last = 0
            for _image in os.listdir(self.viewer_path):
                if _image.endswith('.jpg') and not _image.startswith('.'):
                    image_obj = cv2.imread(os.path.join(self.viewer_path, _image))
                    gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)
                    avg_gray = numpy.average(gray)
                    if last == 0 :
                        last = avg_gray
                    else:
                        if float(avg_gray) - float(last) > float(self.div_val):
                            viewer_frame = _image[-9:-4]
                            break
                    last = avg_gray
        else:
            viewer_frame = 0
        return {'actor': actor_frame, 'viewer': viewer_frame}


class AVSyncDetector(object):
    def __init__(self, frame_path, ambang):
        self.frame_path = frame_path
        self.div_val = ambang

    def process_detect(self, arg_file_name):
        if os.path.exists(self.frame_path):
            last = 0
            frame_nums = []
            for _image in os.listdir(self.frame_path):
                if _image.endswith('.jpg') and not _image.startswith('.'):
                    image_obj = cv2.imread(os.path.join(self.frame_path, _image))
                    gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)
                    avg_gray = numpy.average(gray)
                    if last == 0 :
                        last = avg_gray
                    else:
                        if abs(float(avg_gray) - float(last)) > float(self.div_val):
                            if frame_nums != []:
                                if int(frame_nums[len(frame_nums) -1] + 250) < int(_image[-9:-4]):
                                    frame_nums.append(int(_image[-9:-4]))
                            else:
                                frame_nums.append(int(_image[-9:-4]))
                    last = avg_gray
            return frame_nums
        else:
            actor_frame = 0



def main():
    argpars = argparse.ArgumentParser("检测视频延迟数值输入frame／videodelay,即可间该目录下的每个文件夹中的关键帧")
    argpars.add_argument('--ambang', type=float, default=80.0, desc='灰度阀值，目前默认：80')
    argpars.add_argument('--type', type=str, default='videodelay')
    argpars.add_argument('base_dir')
    args = argpars.parse_args()
    base_dir = args.base_dir
    ambang = args.ambang
    if args.type == 'videodelay':
        with open('result.csv', 'wb') as re_file:
            writer = csv.writer(re_file)
            writer.writerow(['name', 'actor', 'viewer'])
            for _file in os.listdir(base_dir):
                if os.path.isdir((os.path.join(base_dir,_file))):
                    if _file.find('videodelay_actor') > 0:
                        actor_path = os.path.join(base_dir,_file)
                        viewer_path = actor_path.replace('actor', 'viewer')
                        videodetect = VideoDelayDetector(actor_path, viewer_path, ambang)
                        result = videodetect.process_detect()
                        writer.writerow([_file, result['actor'], result['viewer']])
    elif args.type == 'avsync':
        with open('result_av.csv', 'wb') as re_file:
            writer = csv.writer(re_file)
            for _file in os.listdir(base_dir):
                if os.path.isdir((os.path.join(base_dir,_file))):
                    if _file.find('avsync') > 0:
                        print _file
                        frame_path = os.path.join(base_dir, _file)
                        avsync = AVSyncDetector(frame_path, float(30.0))
                        result = avsync.process_detect(_file)
                        re = [_file]
                        re.extend(result)
                        writer.writerow(re)


if __name__ == '__main__':
    main()