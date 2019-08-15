# -*- coding:utf-8 -*-

import subprocess
import os
import sys
import time
import shutil
import subprocess
import math
import ffmpeg
import argparse
import utils
import json

VIDEO_EXE = ['.mp4', '.avi', '.mov']


def _getdefaultencoding():
    if os.name == 'nt':
        return 'gbk'
    else:
        return 'utf-8'


AV_FOLDER_NAME = 'avsync'
AV_WEB = ['game_web', 'game_pc']


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            new = super(Singleton, cls)
            cls._instance = new.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, src_video_path, frames_path, base_backup_dir):
        self.src_video_path = src_video_path
        self.pid_file_name = os.path.basename(os.path.splitext(__file__)[0]) + '.pid'
        self.files_ready = []
        self.archive_videos = []
        self.frames_path = frames_path
        self.base_backup_dir = base_backup_dir
        self.pid_file_path = os.path.join(self.base_backup_dir, self.pid_file_name)
        self.metadata_file_name = 'metaData.txt'

    def process(self):
        try:
            # 检查pid文件是否存在，如果存在结束程序运行
            if os.path.exists(self.pid_file_path):
                sys.exit(1)
            with open(self.pid_file_path, 'w') as f:
                f.write(str(os.getpid()))

            # 扫描源视频文件夹，看视频文件是否准备好
            self.__check_file_status()
            # 解帧已准备好的视频
            self.__exact_videos()
            # 归档视频文件
            self.__archive_videos()
        finally:
            # 最后执行完成后删除pid file
            self.__teardown()

    def house_keep(self):
        self.__remove_backup_images()
        self.__remove_history_frames()

    def __check_file_status(self):
        # 遍历整个视频文件夹，把已准备好的视频加入列表中
        for parent, dirs, files in os.walk(self.src_video_path):
            for _file in files:
                file_path = os.path.join(parent, _file)
                if os.path.splitext(file_path)[1].lower() in VIDEO_EXE:
                    try:
                        with open(file_path, 'rb') as f:
                            pass
                        self.files_ready.append(file_path)
                    except IOError:
                        pass
        time.sleep(2)

    def __exact_videos(self):
        # 没有准备好的视频文件，退出脚本
        if not self.files_ready:
            sys.exit(1)

        while self.files_ready:
            video_path = self.files_ready.pop(0)
            # 再次检查视频是否读,不行跳过
            try:
                with open(video_path, 'rb') as f:
                    pass
            except IOError:
                continue

            tmp_frames_path = str(video_path).replace(self.src_video_path, self.frames_path)
            current_frames_dir = os.path.splitext(tmp_frames_path)[0]
            frame_rate = self.__get_frame_rate(video_path)
            if frame_rate is None:
                continue
            # 检查视频是否有解帧，如果已解帧，删除帧的整个目录
            if os.path.exists(current_frames_dir):
                shutil.rmtree(current_frames_dir)
            parent_path = os.path.dirname(current_frames_dir)
            if os.path.exists(parent_path):
                os.mkdir(current_frames_dir)
            else:
                os.makedirs(current_frames_dir)
            # 给相应的视频解帧
            print ('Begin to extract the vedio {0},extract frame is:{1},frames store dir:{2}'.format(video_path,
                str(frame_rate), current_frames_dir))
            executable_path = os.path.join(os.path.dirname(__file__), 'extract_frames.py')
            cmd = ['python', executable_path,
                   '-r', str(frame_rate),
                   '-t', 'jpg',
                   '--output-dir', current_frames_dir,
                   video_path]
            child = subprocess.Popen(cmd)
            child.wait()
            self.archive_videos.append(video_path)
            # 写入帧信息到相应的帧目录
            metaData_file_path = os.path.join(current_frames_dir, self.metadata_file_name)
            with open(metaData_file_path,'w') as f:
                f.write(json.dumps({'frame_rate':frame_rate},indent=4))
            # 判断是否是音视频同步视频，如果是分离音频到解帧目录,并进行音视频同步检测
            if video_path.find(AV_FOLDER_NAME) != -1:
                self.__extract_audio(video_path, current_frames_dir)
                #if os.path.basename(os.path.dirname(os.path.dirname(current_frames_dir))) not in AV_WEB:
                    #self._avsync_detect(current_frames_dir)

    def __extract_audio(self, video_path, audio_output_path):
        executable_path = os.path.join(os.path.dirname(__file__), 'extract_audio.py')
        cmd = ['python', executable_path,
               '--output-dir', audio_output_path,
               video_path]
        child = subprocess.Popen(cmd)
        child.wait()

    def _avsync_detect(self, video_path):
        executable_path = os.path.join(os.path.dirname(__file__), 'avsync_detect.py')
        cmd = ['python', executable_path,
               video_path]
        child = subprocess.Popen(cmd)
        child.wait()

    def __parse_rate(self, arg_str):
        top = float(arg_str.split('/')[0])
        down = float(arg_str.split('/')[1])
        return top / down

    def __get_frame_rate(self, video_path):
        fps = 120
        ffprobe_path = utils.find_bin('ffprobe', environs=['FFMPEG_HOME'])
        cmd = [ffprobe_path,
               '-v', 'error',
               '-show_entries', 'stream=r_frame_rate,avg_frame_rate',
               '-of', 'json',
               video_path]
        child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        stdout, _ = child.communicate()
        video_info = json.loads(stdout)
        stream_infos = video_info.get('streams', None)
        if stream_infos is None:
            return None

        for stream_info in stream_infos:
            r_frame_rate = stream_info.get('r_frame_rate', None)
            avg_frame_rate = stream_info.get('avg_frame_rate', None)
            if r_frame_rate is None or avg_frame_rate is None:
                continue
            # 判断是否是音频流，如果是舍弃
            if int(str(r_frame_rate).split('/')[1]) == 0:
                continue

            h_r_frame_rate = self.__parse_rate(str(r_frame_rate))
            h_avg_frame_rate = self.__parse_rate(str(avg_frame_rate))

            # 判断是否是固定帧率，如果不是返回帧率120
            if abs(h_r_frame_rate - h_avg_frame_rate) < 1e-7:
                # 调用天花板函数处理数据
                return math.ceil(h_r_frame_rate)
            return fps
        return None

    def __archive_videos(self):
        for archive_video in self.archive_videos:
            archive_video_rel_path = os.path.relpath(archive_video, self.src_video_path)
            backup_video_path = os.path.join(self.base_backup_dir, archive_video_rel_path)
            backup_video_parent_dir = os.path.dirname(backup_video_path)

            # 创建文件夹, 否则会失败
            if not os.path.exists(backup_video_parent_dir):
                os.makedirs(backup_video_parent_dir)

            # 如果目标文件存在, 则删除
            if os.path.exists(backup_video_path):
                os.remove(backup_video_path)

            print('Begin to archive the video {0} to {1}'.format(archive_video, backup_video_path))
            shutil.move(archive_video, backup_video_path)

    def __remove_backup_images(self):
        for root, dirs, files in os.walk(self.base_backup_dir):
            for _file in files:
                image_path = os.path.join(root, _file)
                try:
                    os.remove(image_path)
                    print '{0} is deleted'.format(image_path)
                except OSError as e:
                    pass

    def __remove_history_frames(self):
        for root, dirs, files in os.walk(self.frames_path):
            for _file in files:
                try:
                    if _file.endswith('.jpg') or _file.endswith('.bmp'):
                        shutil.rmtree(root)
                        print '{0} is deleted'.format(root)
                except OSError as e:
                    pass

    def __teardown(self):
        if os.path.exists(self.pid_file_path):
            print('Deleting the pid file:{0}'.format(self.pid_file_path))
            os.remove(self.pid_file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src_video_path', help='video source path')
    parser.add_argument('frames_path', help='frames path')
    parser.add_argument('backup_video_path', help='video backup path')
    parser.add_argument('--house_keep', dest='house_keep', help='clear frames images and backup videos')
    args = parser.parse_args()
    src_video_path = args.src_video_path
    backup_video_path = args.backup_video_path
    frames_path = args.frames_path
    house_keep = args.house_keep
    file_handler = Singleton(src_video_path, frames_path, backup_video_path)
    if house_keep and house_keep.lower() == 'yes':
        file_handler.house_keep()
        return
    file_handler.process()

if __name__ == '__main__':
    main()
