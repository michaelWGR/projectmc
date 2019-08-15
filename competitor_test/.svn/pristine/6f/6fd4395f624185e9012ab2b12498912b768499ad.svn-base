#-*- coding: utf-8 -*-
import zbar
from PIL import Image
import csv
import argparse
import os
import cv2
import json

import wave
import math
import numpy as np
import matplotlib.pyplot as plt 

def qrcode_detect(image):
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    img = Image.open(image).convert('L')
    width, height = img.size
    qrCode = zbar.Image(width, height, 'Y800', img.tobytes())
    scanner.scan(qrCode)
    data = ''
    for s in qrCode:
        data += s.data
    del img
    return data

def read_wave_data(file_path):   
    f = wave.open(file_path,"rb")  
    params = f.getparams()  
    nchannels, sampwidth, framerate, nframes = params[:4]  
    str_data = f.readframes(nframes)  
    f.close()  
    wave_data = np.fromstring(str_data, dtype = np.short)  
    if nchannels == 2:
        wave_data.shape = -1, 2
        wave_data = wave_data.T
    time = np.arange(0, nframes/nchannels)* (1.0/framerate)  
    return wave_data, time, framerate 

def odd_or_even(wave_data, time, time_threshold ):
    data_tmp = wave_data.copy()
    beep_num = 0
    odd_flag = False
    beep_list = []
    max_flag = False
    while beep_num < 3:
        max_index = np.argmax(np.abs(data_tmp))
        if beep_num == 0:
            max_flag = True
        elif beep_num == 1:
            max_flag = False if abs(time[max_index]-beep_list[0]) < time_threshold else True
        elif beep_num == 2:
            if abs(time[max_index]-beep_list[0]) < time_threshold or abs(time[max_index]-beep_list[1]) < time_threshold:
                max_flag = False
            else:
                max_flag = True
                odd_list = [int(beep_list[0])%2, int(beep_list[1])%2, int(time[max_index])%2]
                odd_flag = True if odd_list.count(1) > odd_list.count(0) else False
        if max_flag:
            beep_list.append(time[max_index])
            data_tmp[max_index] = 0
            beep_num += 1
        else:
            data_tmp[max_index] = 0
            continue
    return odd_flag

def max_list(wave_data, time, odd_flag, time_interval, time_threshold):
    data_tmp = wave_data.copy()
    beep_num = 0
    beep_list = []
    index_list = []
    max_flag = False
    max_beepnum = math.ceil(time[time.shape[0]-1]/time_interval)
    while beep_num < max_beepnum:
        max_index = np.argmax(np.abs(data_tmp))
        if odd_flag:
            if beep_num == 0 and not (int(time[max_index])%2 == 0):
                max_flag = True
            else:
                for beep in beep_list:
                    if abs(time[max_index]-beep)<time_threshold or not (int(time[max_index])%2 == 1):
                        max_flag = False
                        break
                    max_flag = True
        else:
            if beep_num == 0 and int(time[max_index])%2 == 0:
                max_flag = True
            else:
                for beep in beep_list:
                    if abs(time[max_index]-beep)<time_threshold or int(time[max_index])%2 == 1:
                        max_flag = False
                        break
                    max_flag = True
        if max_flag:
            beep_list.append(time[max_index])
            index_list.append(max_index)
            data_tmp[max_index] = 0
            beep_num += 1
        else:
            data_tmp[max_index] = 0
            continue
    return sorted(beep_list), sorted(index_list)

def calc_mean(wave_data, low_threshold, up_threshold):
    cond = (np.abs(wave_data) > low_threshold) & (np.abs(wave_data) < up_threshold)
    filter_data = np.extract(cond, wave_data)
    up_mean = np.mean(np.abs(filter_data))
    return up_mean

def get_framerate(args):
    image_path = os.path.abspath(args.image_path)
    metadata_path = os.path.join(image_path, 'metaData.txt')
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            data = json.load(f)
            framerate = data['frame_rate']
    else:
        if args.frame_rate == None:
            print "'please input frame rate, such as '-r 120' " 
            raise ValueError
        else:
            framerate = args.frame_rate
    return framerate

def audio_detect(args):
    low_threshold = args.low_threshold if args.low_threshold is not None else 2500
    time_interval = args.time_interval if args.time_interval is not None else 2
    time_threshold = 0.05
    audio_paths = args.image_path
    audio_list = [os.path.join(audio_paths, file) for file in os.listdir(audio_paths) if file.endswith('.wav') or file.endswith('.WAV')]
    for audio_path in audio_list:
        audio_name = os.path.splitext(audio_path)[0]
        wave_data, time, framerate = read_wave_data(audio_path)
        plt.plot(time, wave_data, color ='blue', linewidth=0.5)
        up_threshold = args.up_threshold if args.up_threshold is not None else np.max(wave_data)
        odd_flag = odd_or_even(wave_data, time, time_threshold )
        beep_maxlist, index_maxlist = max_list(wave_data, time, odd_flag, time_interval, time_threshold)
        up_mean = calc_mean(wave_data, low_threshold, up_threshold)
        print "audio path: ",audio_path ," up_mean: ", up_mean
        beep_startlist = []
        for index in index_maxlist:
            for i in range(index - int(framerate*0.05), index):
                if np.abs(wave_data[i]) < up_mean:
                    continue
                else:
                    start_time = float(int(time[i]*1000))/1000
                    beep_startlist.append(start_time)
                    plt.vlines(start_time, -np.max(np.abs(wave_data)), np.max(np.abs(wave_data)), color ='red', linewidth=1.5, linestyle="--")
                    break
        plt.savefig(audio_name +'.png')
        plt. close('all')
        #plt.show()
        with open(audio_name +'_audio_detect.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for beep in beep_startlist:
                writer.writerow([beep])
        return beep_startlist

def image_detect(args):
    image_path = args.image_path
    image_path = os.path.abspath(image_path)
    image_dir = os.path.dirname(image_path)
    frame_type = args.frame_type if args.frame_type is not None else 'jpg'

    result_csv_path = os.path.join(image_path , os.path.basename(image_path)+'_image_detect.csv')
    filelist = [os.path.join(image_path , file) for file in os.listdir(image_path) if file.endswith(frame_type)]

    results = []
    preresult = 'XX'
    for file_path in filelist:
        output_path = os.path.join(image_path, os.path.basename(file_path))
        result = qrcode_detect(output_path)
        if result !='' and result != preresult:
            print file_path, result, filelist.index(file_path)+1
            results.append((file_path, filelist.index(file_path)+1))
            preresult = result

    with open(result_csv_path, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for (file_path, index) in results:
            writer.writerow((file_path, index))
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', help='frame rate')
    parser.add_argument('-t', '--frame-type', help='frame type')

    parser.add_argument('-lt', '--low-threshold', type=float, help='low threshold')
    parser.add_argument('-ut', '--up-threshold', type=float, help='up threshold')
    parser.add_argument('-dt', '--delay-threshold', type=float, help='the delay threshold of audio and image')
    parser.add_argument('-ti', '--time-interval', type=float, help='time interval')

    parser.add_argument('image_path')
    args = parser.parse_args()

    framerate = get_framerate(args)
    delay_threshold = args.delay_threshold if args.delay_threshold is not None else 1
    audio_start_time = audio_detect(args)
    image_start_picture = image_detect(args)

    image_path = os.path.abspath(args.image_path)
    result_csv_path = os.path.join(image_path, os.path.basename(image_path)+'_avsync_result.csv') 

    pictime_cor_audiotime = []
    for start_time in audio_start_time:
        for start_picture in image_start_picture:
            image_start_time = float(start_picture[1])/framerate
            if abs(start_time - image_start_time) <= delay_threshold:
                pictime_cor_audiotime.append((start_picture[0], start_picture[1], start_time))

    with open(result_csv_path, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for (file_path, index, time) in pictime_cor_audiotime:
            writer.writerow((file_path, index, time))

if __name__ == '__main__':
    main()