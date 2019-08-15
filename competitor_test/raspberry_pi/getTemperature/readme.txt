python getTemperature.py 
将传感器的温度输出到屏幕，ctrl+c停止运行

python getTemperature.py -t 1 
监测1分钟的温度，结果存储到当前目录下，文件名为开始时间+传感器名称（如2016-06-03_17:43:11_6A.csv)

python getTemperature.py -t 1 -s test 
监测1分钟的温度，结果存储到以test为前缀的文件中，如test_6A、test_6B，每个传感器一个文件
