# -*- coding:utf-8 -*-

import os
import subprocess as sp
import sys

import numpy


def print_help():
    print u"用法 python wavParse.py -s 音频路径名"
    print u"选项："
    print u"\t -h/--help 帮助"
    print u"tips:文件名中间不要有空格"
    print u"\t -s 原视频地址"
    print u"\t -a 设定开始时的阈值，默认150"
    print u"\t -d 设定结束时的阈值，默认5"
    print u"\t -r 设定采样率，默认44100"
    print u"\t -t 设定断点时间阈值，默认0.5"
    print u"\t -n 设定相隔时间阈值，默认4.8"
    print u"\t -l 设定音频段长度，默认为9.8"


def getparams():
    global param_source_file
    global example_rate
    global ap
    global de_ap
    global break_time
    global interval_time
    global audio_length
    example_rate = ap = de_ap = break_time = interval_time = audio_length = -1

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-h" or sys.argv[i] == "--help":
            print_help()
            sys.exit(0)
        elif sys.argv[i] == "-s":
            i += 1
            if os.path.isdir(sys.argv[i]):
                param_source_file = sys.argv[i]
            else:
                print_help()
                sys.exit(0)
        elif sys.argv[i] == '-a':
            i += 1
            ap = sys.argv[i]
        elif sys.argv[i] == '-d':
            i += 1
            de_ap = float(sys.argv[i])
        elif sys.argv[i] == '-r':
            i += 1
            example_rate = float(sys.argv[i])
        elif sys.argv[i] == '-t':
            i += 1
            break_time = float(sys.argv[i])
        elif sys.argv[i] == '-n':
            i += 1
            interval_time = float(sys.argv[i])
        elif sys.argv[i] == '-l':
            i += 1
            audio_length = float(sys.argv[i])
        else:
            print u"你输入了错误的参数(-。-)"

    example_rate = example_rate if example_rate != -1 else 44100
    ap = float(ap) if ap != -1 else float(200)
    de_ap = float(de_ap) if de_ap != -1 else float(20)
    break_time = float(break_time) if break_time != -1 else float(0.5)
    interval_time = float(interval_time) if interval_time != -1 else float(4.8)
    audio_length = float(audio_length) if audio_length != -1 else float(9.8)


def extarct(ffmpeg_tool_path):
    global param_source_file
    global example_rate
    global break_time
    global ap
    global interval_time
    global de_ap
    global audio_length

    list = os.listdir(param_source_file)
    for line in list:
        if line.endswith('.wav') or line.endswith('.mp3'):
            command = [ os.path.join(ffmpeg_tool_path, 'ffmpeg'),
            '-i', os.path.join(param_source_file, line),
            '-f', 's16le',
            '-acodec', 'pcm_s16le',
            '-ar', int(example_rate).__str__(), # ouput will have 44100 Hz
            '-ac', '2', # stereo (set to '1' for mono) 声道选项
            '-']
            pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
            raw_audio = pipe.stdout.read()

            audio_array = numpy.fromstring(raw_audio, dtype="int16")
            print len(audio_array)
            audio_array = audio_array.reshape((len(audio_array)/2, 2))
            print u"采样总数：%d" %(len(audio_array))

            flag1 = 1
            flag2 = 1
            break_count = 0     #计算断点数
            # block_count = 0     #计算块数
            pre_example = -1    #前置采样点
            pre_flag = -1       #开始采样点
            result_array = []        #结果数组


            count = 0
            for i in range(189120, 195000):
                if abs(audio_array[i][0]) > 0:
                    print audio_array[i][0]
                    count+=1
                if count ==10:
                    break;
            # exit(0)
            for i in range(1, len(audio_array)):
                if abs(audio_array[i][0]-audio_array[i-1][0]) > ap:
                    if flag2 == 1:
                        if pre_example != -1:
                            if float(i-pre_example)/example_rate < break_time:
                                break_count += 1
                        flag2 = 0
                        pre_example = i

                    if flag1 == 1:
                        size = len(result_array)
                        if size>0:
                            if float(i-result_array[size-1])/example_rate < interval_time:
                                continue

                        if size > 0 and i-result_array[size-1] < break_time * example_rate:
                            result_array.remove(result_array[size-1])
                            flag1 = 0
                            continue
                        #设置间隔
                        # pre_flag = i
                        flag1 = 0
                        result_array.append(i)
                        # print u"音频开始：%lf" % (float(i)/example_rate)


                elif abs(audio_array[i][0]-audio_array[i-1][0]) < de_ap and abs(audio_array[i][0]) == 0:
                    if flag2 == 0:
                        flag2 = 1
                        pre_example = i

                    if flag1 == 0:
                        size = len(result_array)
                        #设置间隔
                        if size > 0:
                            if float(i-result_array[size-1])/example_rate < audio_length:
                                continue

                        # next_start_frame = -1
                        # for j in range(i+1, i+int(example_rate*break_time)):
                        #     if abs(audio_array[j][0]-audio_array[j-1][0]) > ap:
                        #         next_start_frame = j
                        #         break
                        # if next_start_frame != -1 and (next_start_frame-i)/example_rate < break_time:
                        #     continue

                        # pre_flag = i
                        result_array.append(i)
                        flag1 = 1
                        # block_count += 1
                        # print u"音频结束：%lf" % (float(i)/example_rate)

            for i in range(0,len(result_array)):
                if i & 1 == 1:
                    print u"音频结束：%lf" % (float(result_array[i])/example_rate)
                if i & 1 == 0:
                    print u"音频开始：%lf" % (float(result_array[i])/example_rate)
            print u"断点数：%d" % (break_count)
            print u"块数：%d" % (int(len(result_array))/2)
            print "interval_time=%f" % interval_time



if __name__ == "__main__":
    print u"请确认已经配置了ffmpeg的环境变量FFMPEG_HOME（-m -）"
    ffmpeg_path = os.getenv('FFMPEG_HOME')

    print ffmpeg_path
    if os.path.isdir(ffmpeg_path):
        ffmpeg_tool_path = os.path.join(ffmpeg_path, "bin")
    else:
        print u"请先设置'FFMPEG_HOME'环境变量"
        sys.exit(0)

    getparams()
    extarct(ffmpeg_tool_path)

