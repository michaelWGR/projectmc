# -*- coding:utf-8 -*-
import csv
import os
import sys
import argparse


def get_file(files_path):
    '''
    获取当前文件夹内视频的路径
    '''

    if not os.path.exists(files_path):
        raise Exception("{0} is not exist".format(files_path))
    for _, dirs, files in os.walk(files_path):
        videos_to_proc = []
        for file in files:
            if file.endswith('.mp4') or file.endswith('.MOV') or file.endswith('.mov'):
                abspath = os.path.join(files_path,file)
                videos_to_proc.append(abspath)
        return videos_to_proc

def run_script(script_path, fps, file):
    '''
    运行流畅度脚本，解析一个视频
    '''

    if not os.path.exists(script_path):
        raise Exception("{0} is not exist".format(script_path))
    cmd = 'python ' + script_path + ' -r {0} '.format(fps) + file
    os.system(cmd)

def get_resultsfile(files_path):
    '''
    获取当前文件夹里所有的result的csv文件
    '''
    for _, dirs, files in os.walk(files_path):
        results_to_proc = []
        for resultfile in files:
            if resultfile.endswith('.csv') and ('_result' in resultfile):
                abspath = os.path.join(files_path,resultfile)
                results_to_proc.append(abspath)
        return results_to_proc

def get_averesult(result_file):
    '''
    通过result文件来计算平均值
    '''

    if not os.path.exists(result_file):
        raise Exception("{0} is not exist".format(result_file))
    result_list = []
    with open(result_file, 'rb') as resultfile:
        reader = csv.reader(resultfile)
        for result in reader:
            result_list.append(result[1])
        result_list = result_list[0: len(result_list)-2]
        result_list = [int(value) for value in result_list]
        return float(sum(result_list))/len(result_list)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', type=float, help='frame rate')
    parser.add_argument('-s', '--script-path')

    parser.add_argument('--only-getresult', action='store_true', default=False, help='only get result')
    parser.add_argument('files_path')
    args = parser.parse_args()

    script = r'/Users/yyinc/Documents/guirong/competitor_test/fluency/fluency_detector.py'

    frame_rate = args.frame_rate if args.frame_rate is not None else 60
    script_path = args.script_path if args.script_path is not None else script
    only_getresult = args.only_getresult
    files_path = args.files_path

    with open(files_path + '_result.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        if not only_getresult:
            video_list = get_file(files_path)
            if len(video_list) == 0:
                print 'no file to be processed!!'
                sys.exit()

            for file in video_list:           
                print file
                if not os.path.exists(os.path.splitext(file)[0]+'_result.csv'):
                    run_script(script_path, frame_rate, file)
            
            result_list = get_resultsfile(files_path)
            if len(result_list) == 0:
                print 'no result file to be process!!'
                sys.exit()

            for resultfile in result_list:
                averesult = get_averesult(resultfile)
                writer.writerow((resultfile, averesult))

        else:
            result_list = get_resultsfile(files_path)
            if len(result_list) == 0:
                print 'no result file to be process!!'
                sys.exit()

            for resultfile in result_list:
                averesult = get_averesult(resultfile)
                writer.writerow((resultfile, averesult))

if __name__ == '__main__':
    # main()
    result_file = '/Users/yyinc/Documents/guirong/projectmc/fluency/video/opr11dyin_android_productionfluency_01_result.csv'
    print get_averesult(result_file)