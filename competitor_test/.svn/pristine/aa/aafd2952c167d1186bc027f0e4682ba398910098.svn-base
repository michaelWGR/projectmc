# 流畅度计算

## 环境准备

1. Python 2.7或者以上

2. opencv2

3. numpy

4. tesseract，设置`TESSERACT_HOME`环境变量

5. ffmpeg，设置`FFMPEG_HOME`环境变量

## 执行步骤

### 数字识别

执行脚本`number_detector.py`完成下面的事情：
1. 解帧并且去重，存到`${video_name}`的文件夹下
2. 切割出数字部分，并另存为到`${video_name}_roi`的文件夹下
3. 识别出数字，结果存到`${video_name}_number.csv`

**注意：**

1. 不同平台切割参数不同，请使用`--roi-type`参数指定，目前只有`android`和`ios`
2. 如果图片有奇怪的噪点，tesseract可能会识别出奇怪的字符，为了方便查问题，这里并不去掉

#### 输入单个视频

```shell
python number_detector.py -r 60 --roi-type android /path/to/video.mp4
```

#### 输入多个视频

Linux / OSX / Unix
```shell
ls *.mp4 | xargs python number_detector.py -r 60 --roi-type android
```

Windows
请使用`number_detector.bat`，最后一个参数使用通配符
```bat
number_detector.bat -r 60  --roi-type android C:\path\to\video\*.avi
```

#### 执行单个步骤
脚本分为解帧（包括去重）、切割、识别三个步骤。
如果需要执行其中一个步骤，可以使用`--just-${step}`参数。
但要注意的是，要确保前一个步骤，已经执行成功。

解帧
```shell
python number_detector.py -r 60 --just-extract --roi-type android /path/to/video.mp4
```

切割
```shell
python number_detector.py -r 60 --just-roi --roi-type android /path/to/video.mp4
```

识别
```shell
python number_detector.py -r 60 --just-detect --roi-type android /path/to/video.mp4
```

### 流畅度计算
执行脚本`fluency_calculate.py`，结果输出为`${video_name}_result.csv`
**注意：**脚本在解析数字的时候，会忽略数字之间的空格，因为tesseract可能会认为数字间距太大而存在空格

#### 输入单个数字识别结果

```shell
python fluency_calculate.py /path/to/video/video_name_number.csv
```

#### 输入多个数字识别结果

Linux / OSX / Unix
```shell
ls *_number.csv | xargs python fluency_calculate.py
```

Windows
请使用`fluency_calculate.bat`，最后一个参数使用通配符
```bat
fluency_calculate.bat C:\path\to\video\*_number.csv
```