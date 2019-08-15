# -*- coding:utf-8 -*-

import os
import sys
import csv
import subprocess
import utils


def get_packet_infos(video_path):
    import json

    ffprobe_path = utils.find_bin('ffprobe')

    cmd = [ffprobe_path,
           '-v', 'error',
           '-select_streams', 'v',
           '-show_packets',
           # '-show_entries', 'frame=pict_type,pkt_pts,pkt_pts_time,pkt_duration_time',
           '-of', 'json',
           video_path]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = child.communicate()

    video_info = json.loads(stdout)
    packet_infos = video_info.get('packets', None)
    if packet_infos is not None:
        packet_num = 0
        for packet_info in packet_infos:
            packet_num += 1
            yield packet_num, packet_info

    child.poll()


def get_frame_infos(video_path):
    import json

    ffprobe_path = utils.find_bin('ffprobe')

    cmd = [ffprobe_path,
           '-v', 'error',
           '-select_streams', 'v',
           '-show_frames',
           '-show_entries', 'frame=pict_type,pkt_pts,pkt_pts_time,pkt_duration_time,pkt_size',
           '-of', 'json',
           video_path]
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = child.communicate()

    video_info = json.loads(stdout)
    frame_infos = video_info.get('frames', None)
    if frame_infos is not None:
        frame_num = 0
        for frame_info in frame_infos:
            frame_num += 1
            yield frame_num, frame_info

    child.poll()


def main():
    for video_path in sys.argv[1:]:
        # video_path = os.path.abspath(sys.argv[1])
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        video_frames_csv = os.path.join(video_dir, video_name + '_frames.csv')

        with open(video_frames_csv, 'wb') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['frame_num', 'pict_type', 'pkt_size', 'pkt_duration_time', 'pkt_pts', 'pkt_pts_time'])
            for frame_num, frame_info in get_frame_infos(video_path):
                csv_writer.writerow([
                    frame_num,
                    frame_info.get('pict_type', ''),
                    frame_info.get('pkt_size', ''),
                    frame_info.get('pkt_duration_time', ''),
                    frame_info.get('pkt_pts', ''),
                    frame_info.get('pkt_pts_time', ''),
                ])


if __name__ == '__main__':
    main()
