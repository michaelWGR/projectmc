# -*- coding:utf-8 -*-
import subprocess
import argparse
import time


def main():
    argparser = argparse.ArgumentParser('android collect 6 fluency video')
    # argparser.add_argument('-device', default=None)
    argparser.add_argument('app')
    args = argparser.parse_args()
    app_name = args.app
    for i in range(1,4):
        print 'start collect ' + str(i)
        video_name = app_name + '_android_fluency_0' + str(i) + '.mp4'
        # if arg.device is None:
        cmd = ['adb', 'shell', 'screenrecord', '--bit-rate', '8000000', '--size', '720x1280','/sdcard/yypm/fluency/' + video_name]
        # else:
            # cmd = ['adb', '-s', arg.device, 'shell', 'screenrecord', '--bit-rate', '8000000', '/sdcard/yypm/fluency/' + app_name + '_android_fluency_0' + str(i) + '.mp4']
        p = subprocess.Popen(cmd)
        time.sleep(125)
        p.kill()
        print 'finish collect ' + str(i)

        print 'pull video ' + str(i)
        time.sleep(2)
        cmd = ['adb', 'pull', '/sdcard/yypm/fluency/' + video_name]
        p = subprocess.Popen(cmd)
        p.wait()

        print 'delete video' + str(i)
        cmd = ['adb', 'shell', 'rm', '/sdcard/yypm/fluency/' + video_name]
        p = subprocess.Popen(cmd)
        p.wait()

if __name__ == '__main__':
    main()