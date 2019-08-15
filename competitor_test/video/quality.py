# encoding: utf-8

import os
import time
import argparse


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_time(inputScript):
    StartTime = time.clock()
    try:
        os.system(inputScript)
    except Exception as e:
        print e
    return str(time.clock()-StartTime)

def write_time(scriptDic, timeFilePath):
    timeDic = {}
    timeDic['totaltime']= 0
    for key in sorted(scriptDic.keys()):
        timename = key+'Time'
        timeDic[timename] = run_time(scriptDic[key])
        timeDic['totaltime'] += float(timeDic[timename])
    for timekey in sorted(timeDic.keys()):
        print '{0}: {1}/n'.format(timekey, timeDic[timekey])
    with open(timeFilePath,'w') as timefile:
        for timekey in sorted(timeDic.keys()):
            timefile.write('{0}: {1} sec = {2} min/n'.format(timekey, timeDic[timekey], str(float(timeDic[timekey])/60)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',default=False, help='verbose')
    parser.add_argument('-r', '--frame-rate', type=float, help='frame rate')
    parser.add_argument('-t', '--frame-type', help='frame type')
    parser.add_argument('--level', type=int, help='mip map level')
    parser.add_argument('-nb', '--not-bs', action='store_true', default=False, help='dont use binary search')

    parser.add_argument('--just-process_source', action='store_true', default=False, help='just process source video')
    parser.add_argument('--just-del_source', action='store_true', default=False, help='just delete source gray frames')
    parser.add_argument('--just-process_stream', action='store_true', default=False, help='just process catched stream')
    parser.add_argument('--just-del_stream', action='store_true', default=False, help='just delete gray frames')
    parser.add_argument('--just-cut_source', action='store_true', default=False, help='just cut source frames')
    parser.add_argument('--just-mipmap', action='store_true', default=False, help='just mip map')
    parser.add_argument('--just-align', action='store_true', default=False, help='just align')
    parser.add_argument('--just-ssim', action='store_true', default=False, help='just ssim')

    parser.add_argument('-s', '--sourceVideo', help='source Video file')
    parser.add_argument('streamsDir')
    args = parser.parse_args()

    frame_rate = args.frame_rate if args.frame_type is not None else 60
    frame_type = args.frame_type if args.frame_type is not None else 'bmp'
    level = args.level if args.level is not None else 5
    not_bs = args.not_bs

    sourceVideo = os.path.abspath(args.sourceVideo)
    video_name = os.path.splitext(os.path.basename(sourceVideo))[0]
    source_frames_dir_path = os.path.join(os.path.dirname(sourceVideo), video_name)
    streamsDir = args.streamsDir

    # 处理原始视频：先解帧，后去灰帧
    if sourceVideo is None:
        print "No input source video!"
        raise IOError


    sourceExtract = r'python {0} -r {1} -t {2} {3}'.format(os.path.join(BASE_DIR, 'extract_frames.py'), frame_rate, frame_type, sourceVideo)
    if not_bs:
        delSourcegray = r'python {0} {1}'.format(os.path.join(BASE_DIR, 'delete_grayframes.py'), source_frames_dir_path)
    else:
        delSourcegray = r'python {0} {1}'.format(os.path.join(BASE_DIR, 'delGrayframes_bs.py'), source_frames_dir_path)

    source_just_flags = (just_proceSource, just_delSource) = (args.just_process_source, args.just_del_source)
    assert sum(1 for _ in source_just_flags if _) <= 1
    do_proceSource, do_delSource = source_just_flags

    if os.path.exists(source_frames_dir_path) and len(os.listdir(source_frames_dir_path)) != 0:
        sourceDic={'B_delSourcegray':delSourcegray}
    else:
        if do_proceSource:
            sourceDic={'A_sourceExtract':sourceExtract}
        elif do_delSource:
            sourceDic={'B_delSourcegray':delSourcegray}
        else:
            sourceDic = {
                        'A_sourceExtract':sourceExtract,
                        'B_delSourcegray':delSourcegray
                        }
    sourceTimefile =source_frames_dir_path+'_runtime.txt'
    write_time(sourceDic, sourceTimefile)

    # 处理抓流视频
    filelist = [os.path.join(streamsDir, file) for file in os.listdir(streamsDir) if file.endswith('.flv') or file.endswith('.FLV')]
    if len(filelist) == 0:
        print "No catched stream or the stream is not end with 'flv'!"
        raise IOError

    for catchedStream in filelist:
        name_split = os.path.basename(catchedStream).split('_')
        if name_split[1].strip() not in ['android', 'ios']:
            print "the name of catched stream is undesirable!"
            raise IOError
        roi_param = name_split[0].strip()+'_'+name_split[1].strip()
        roi_param_source = roi_param+'_source'

        stream_just_flags = (just_proceStream, just_delStream, just_cutSource, just_mipmap, just_align, just_ssim) \
                = ( args.just_process_stream, args.just_del_stream, args.just_cut_source, args.just_mipmap, args.just_align, args.just_ssim)
        assert sum(1 for _ in stream_just_flags if _) <= 1
        do_proceStream, do_delStream, do_cutSource, do_mipMap, do_align, do_ssim = stream_just_flags

        catchedName = os.path.join(os.path.dirname(catchedStream),os.path.splitext(os.path.basename(catchedStream))[0])
        streamtimefile = catchedName+'_runtime.txt'

        sourceName_roi = source_frames_dir_path+'_'+roi_param_source+'_roi'
        catchedName_roi = catchedName+'_'+roi_param+'_roi'
        catchedName_roi_csv = catchedName_roi+'.csv'

        if os.path.exists(catchedName_roi+'_result.csv'):
            continue

        #分6步：处理抓流视频、去灰帧、切源帧、缩小源帧、对帧、SSIM
        procStream = r'python {0} -r {1} -t {2} -d True --roi-type {3} {4}'.format(
                os.path.join(BASE_DIR, 'etr_rm_cut.py'), frame_rate, frame_type, roi_param, catchedStream
            )
        if not_bs:
            delStream = r'python {0} {1}'.format(os.path.join(BASE_DIR, 'delete_grayframes.py'), catchedName_roi)
        else:
            delStream = r'python {0} {1}'.format(os.path.join(BASE_DIR, 'delGrayframes_bs.py'), catchedName_roi)
        cutSource = r'python {0} --roi-type {1} {2}'.format(os.path.join(BASE_DIR, 'image_process.py'), roi_param_source, source_frames_dir_path)
        mipMap = r'python {0} --level {1} {2}'.format(os.path.join(BASE_DIR, 'mip_map.py'), level, sourceName_roi)
        align = r'python {0} --level {1} {2} {3}'.format(os.path.join(BASE_DIR, 'align_frames.py'), level, sourceName_roi, catchedName_roi)
        ssim = r'python {0} {1}'.format(os.path.join(BASE_DIR, 'run_ssim_by_dirs.py'), catchedName_roi_csv)

        if do_proceStream:
            streamDic={'A_procStream': procStream}

        elif do_delStream:
            streamDic={'B_delStream': delStream}

        elif do_cutSource:
            streamDic={'C_cutSource': cutSource}

        elif do_mipMap:
            streamDic={'D_mipMap': mipMap}

        elif do_align:
            streamDic={'E_align': align}

        elif do_ssim:
            streamDic={'F_ssim': ssim}

        else:
            if os.path.exists(sourceName_roi) and not os.path.exists(os.path.join(sourceName_roi,'mip_map')):
                streamDic={
                    'A_procStream': procStream,
                    'B_delStream': delStream,
                    'D_mipMap': mipMap,
                    'E_align': align,
                    'F_ssim': ssim
                    }
            if os.path.exists(sourceName_roi) and os.path.exists(os.path.join(sourceName_roi,'mip_map')):
                streamDic={
                    'A_procStream': procStream,
                    'B_delStream': delStream,
                    'E_align': align,
                    'F_ssim': ssim
                    }
            else:
                streamDic={
                        'A_procStream': procStream,
                        'B_delStream': delStream,
                        'C_cutSource': cutSource,
                        'D_mipMap': mipMap,
                        'E_align': align,
                        'F_ssim': ssim
                        }
        write_time(streamDic, streamtimefile)

if __name__ == '__main__':
    main()

