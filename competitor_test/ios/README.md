# iOS Trace文件分析

## 环境准备

1. Python 2.7或者以上
2. XCode Version 7.3.1 (7D1014)

## CPU

执行脚本`parse_trace_cpu.py`分析指定进程的CPU数据。

脚本会调用同级文件夹下的可执行文件`TraceUtility`对输入的Trace文件进行分析，获取指定进行的CPU数据。

### 命令行

```shell
python parse_trace_cpu.py ${process_name} /path/to/trace [[/path/to/trace] ... ]
```

### 输入

`${process_name}`，进程名，具体查看Trace文件中的`Process Name`

`/path/to/trace`，Trace文件路径，可以多个

### 输入多个Trace文件

Linux / OSX / Unix

```shell
ls -d *.trace | xargs parse_trace_cpu.py ${process_name} 
```

Windows

暂时不支持

### 输出

结果会输出到`/path/to/trace`同级文件夹下的两个CSV文件，分别是：

1. `${filename}_${process_name}_cpu.csv`，进程名为`${process_name}`的进程CPU状况
2. `${filename}_mediaserverd_cpu.csv`，进程名为`mediaserverd`的进程CPU状况

输出的CSV格式是：

除了最后一行之外

```
SampleNumber, Command, CPUUsage
```

最后一行

```
-, -, AverageCPUUsage, STDEVCPUUsage
```


例如：

```shell
python parse_trace_cpu.py kiwi /path/to/example.trace
```

结果输出到`/path/to/example_kiwi_cpu.csv`和`/path/to/example_mediaserverd_cpu.csv`

## GPU

执行脚本`parse_trace_gpu.py`分析GPU数据

脚本会调用同级文件夹下的可执行文件`TraceUtility_gpu`对输入的Trace文件进行分析，获取GPU数据。

### 命令行

```shell
python parse_trace_gpu.py /path/to/trace [[/path/to/trace] ... ]
```

### 输入

`/path/to/trace`，Trace文件路径，可以多个

### 输入多个Trace文件

Linux / OSX / Unix

```shell
ls -d *.trace | xargs parse_trace_gpu.py 
```

Windows

暂时不支持

### 输出

结果会输出到`/path/to/trace`同级文件夹下的CSV文件`${filename}_gpu.csv`

输出的CSV格式是：

除了最后一行之外

```
Device Utilization, Tiler Utilization
```

最后一行

```
-, -, AverageGPUUsage, STDEVGPUUsage
```

例如：

```shell
python parse_trace_gpu.py /path/to/example.trace
```

结果输出到`/path/to/example_gpu.csv`

## 网络流量

执行脚本`parse_trace_network.py`分析网络流量数据。

脚本会遍历Trace文件（Trace文件事实上是一个文件夹）下面的所有`.netconndb`文件，利用`sqlite`分析`.netconndb`文件获取网络流量数据。

### 命令行

```shell
python parse_trace_network.py /path/to/trace [[/path/to/trace] ... ]
```

### 输入

`/path/to/trace`，Trace文件路径，可以多个

### 输入多个Trace文件

Linux / OSX / Unix

```shell
ls -d *.trace | xargs parse_trace_cpu.py 
```

Windows

暂时不支持

### 输出

结果会输出到`/path/to/trace`同级文件夹下的`N`个CSV文件，`${filename}_${run_name}_network.csv`。

其中，`${run_name}`一般情况下只有一个且是`Trace1`，但因为Trace文件里面可以包含多个Run（采集一次就是一个Run），所以可能会包含多个`${run_name}`。

输出的CSV格式是：

除了最后两行之外

```
time, rx_bytes, tx_bytes
```

最后第二行

```
-, total_rx_mb, total_tx_mb
```

最后第一行

```
-, avgerage_rx_kb, avgerage_tx_kb
```

其中，`rx`是下行，`tx`是上行

例如：

```shell
python parse_trace_cpu.py /path/to/example.trace
```

结果输出到`/path/to/example_Trace1_network.csv`

## 