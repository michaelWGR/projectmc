# 移动直播流畅度算法

## 环境准备

1. Python 2.7或者以上
2. opencv2
3. numpy
4. ffmpeg，设置`FFMPEG_HOME`环境变量

## 脚本说明

```shell
python fluency_detector.py /path/to/${video_name}.${ext}
```

执行脚本完成下面的事情：

1. 解帧，存到`/path/to/${video_name}`文件夹下
2. 识别进度，结果存到`/path/to/${video_name}_progress.csv`文件中
3. 计算流畅度，结果存到`/path/to/${video_name}_number.csv`

### 输入

- `/path/to/${video_name}.${ext}`

  ​

### 输出

- `/path/to/${video_name}`

  解帧文件夹

- `/path/to/${video_name}_progress.csv`

  进度识别结果

- `/path/to/${video_name}_number.csv`

  流畅度结果

### 调试

```shell
python fluency_detector.py -d -n ${frame_num} /path/to/frames
```





## 算法说明

### 基本流程

