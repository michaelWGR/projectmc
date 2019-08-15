### 关于本目录
    该目录脚本，主要目的是：采集Android-App的性能数据。在App运行时，采集如：cpu占用，内存占用，流量使用的数据。

### 运行要求
    运行本目录脚本前，请先按要求（http://docs.yypm.com/video_test/labEnvironmentSet/），配置本机开发环境！

### 文件列表说明
- getAndroidBatteryTemperature: 获取Android-电池温度（内部传感器）
- getAndroidCpu: 获取Android-目标进程CPU占用
- getAndroidCpuTemperature: 获取Android-CPU温度（内部传感器）
- getAndroidGPU: 获取Android-GPU占用（仅支持高通CPU系列）
- getAndroidMemery: 获取Android-目标进程内存占用
- getAndroidNetwork: 获取Android-目标进程网络占用
- getMediaServer: 获取Android-mediaserver进程cpu占用
- run.py: 实际监控时，会运行run.py，它会调用以上相关的监控文件，采集性能数据。（注意，run不一定采集所有以上类型的性能数据！）
- summary: 整合以上监控的结果文件

### 参数说明（每个 监控脚本 传入参数一致，格式如下：）
- 第一个参数：采集信息间隔时间
- 第二个参数：日志文件的放置位置
- 第三个参数：应用的包名

|脚本名称|备注|
|-------|---|
|getAndroidCpu|需要输入3个参数|
|getAndroidMemery|需要输入3个参数|
|getAndroidNetwork|需要输入3个参数|
|getAndroidbatteryTemperature|输入2个参数：时间间隔、日志位置|
|getAndroidCpuTemperature|输入2个参数：时间间隔、日志位置|