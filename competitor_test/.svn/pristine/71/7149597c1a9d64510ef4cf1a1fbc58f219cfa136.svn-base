# -*- coding:utf-8 -*-

import os
import json
import csv
import collections
import pylab

# 根据日志文件生成对应的csv文件
def log2csv(file_path):
    csv_path = file_path[:len(file_path) - 4] + ".csv"
    arg_floder_name = os.path.basename(file_path)

    with open(csv_path, "ab") as write_file:
        with open(file_path, "r") as contents:
            line = contents.readline()
            while(line):
                message_item = line.split("|")[1]
                jsondata = json.loads(message_item)

                # cpu占用
                if file_path.endswith("_CPU.log") or file_path.endswith("_cpu.log"):
                        csv_writer = csv.writer(write_file)
                        csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["cpu"][:-1]])

                if file_path.endswith("_GPU.log") or file_path.endswith("_gpu.log"):
                    
                        csv_writer = csv.writer(write_file)
                        csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1], jsondata["G01"][:],
                                                 jsondata["G02"][:], jsondata["Load"][:-1], jsondata["Frequency"][:-3]])
                 # 网络
                if file_path.endswith("_network.log"):
                        csv_writer = csv.writer(write_file)
                        csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["second"][:], jsondata["rec_data"][:-1],jsondata["send_data"][:-1]])

                # # 内存
                # if item.endswith("_memory.log"):
                #     with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                #         csv_writer = csv.writer(write_file)
                #         csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["memory"][:-1]])

                # # 电池
                # if item.endswith("_battery.log"):
                #     with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                #         csv_writer = csv.writer(write_file)
                #         csv_writer.writerow([line.split("|")[0][1:len(line.split("|")[0]) - 1],jsondata["battery_temperature"]])
                # cpu温度
                # if item.endswith("e_cpu.log"):
                #     temp = []
                #     temp.append(line.split("|")[0][1:len(line.split("|")[0]) - 1])
                #     sort_item = sorted(jsondata.items(), key=lambda x: int(x[0][4:len(x[0])]))
                #     for _,val in sort_item:
                #         temp.append(val)
                #     with open(item_path[:len(item_path) - 4] + ".csv", "ab") as write_file:
                #         csv_writer = csv.writer(write_file)
                #         csv_writer.writerow(temp)
                line = contents.readline()

    if file_path.endswith("_CPU.log") or file_path.endswith("_cpu.log"):
        summary_cpu(csv_path)

    if file_path.endswith("_GPU.log") or file_path.endswith("_gpu.log"):
        summary_gpu(csv_path)

    if file_path.endswith("_network.log"):
        summary_network(csv_path)

#计算CPU平均占用率
def summary_cpu(file_path):
    temp = 0.0
    if file_path.endswith("_CPU.csv") or file_path.endswith("_cpu.csv"):
        with open(file_path,'rb+') as file_:
            reader = csv.reader(file_)
            load = [float(row[1]) for row in reader]
            temp = (sum(load)/len(load))
            writer = csv.writer(file_)
            writer.writerow(["AVG", temp])

#计算GPU平均占用率
def summary_gpu(file_path):
    temp = 0.0
    if file_path.endswith("_GPU.csv") or file_path.endswith("_gpu.csv"):
        with open(file_path,'rb+') as file_:
            reader = csv.reader(file_)
            load = [float(row[3]) for row in reader]
            temp = (sum(load)/len(load))
            writer = csv.writer(file_)
            writer.writerow(["AVG", ' ', ' ', temp])

# 计算总共使用的流量数据单位M
def summary_network(file_path):
    temp = 0.0
    if file_path.endswith("network.csv"):
        with open(file_path,'rb+') as file_:
            reader = csv.reader(file_)
            second = []
            rec_data = []
            send_data = []

            for row in reader:
                second.append(float(row[1]))
                rec_data.append(float(row[2]))
                send_data.append(float(row[3]))

            interval_second = (second[len(second) - 1] - second[0])

            rec_diff = (rec_data[len(rec_data) - 1] - rec_data[0])/1024
            rec_rate = round(rec_diff/interval_second, 2)

            send_diff = (send_data[len(send_data) - 1] - send_data[0])/1024
            send_rate = round(send_diff/interval_second, 2)

            writer = csv.writer(file_)
            writer.writerow(["AVG", str(interval_second), str(rec_rate)+"KB/s", str(send_rate)+"KB/s",])

# 绘制某一列的走势图
def print_chart(file_path,arg_floder_name,arg_chart_path):
    for item in os.listdir(file_path):
        if item.endswith("_network.csv"):
            item_path = os.path.join(file_path,item)
            count = 1
            x = []
            y = []
            with open(item_path, 'rb') as network_file:
                reader = csv.reader(network_file)
                for row in reader:
                    y.append(float(row[1]))
                    x.append(count)
                    count += 1


                point = dict(zip(x, y))
                point_set = collections.OrderedDict(sorted(point.items()))
                pylab.plot(point_set.keys(), point_set.values(), 'b')
                pylab.title('brisque')
                pylab.savefig(os.path.join(arg_chart_path, arg_floder_name +".png"), dpi=200)
                pylab.clf()

# 获取电池温度起始温度
def get_bettery_tempreture(file_path,arg_floder_name,arg_csv_path):
    for item in os.listdir(file_path):
        if item.endswith("temperature_battery.csv"):
            item_path = os.path.join(file_path,item)
            with open(item_path,'rb') as battery_file:
                reader = csv.reader(battery_file)
                for row in reader:
                    if ( reader.line_num > 1):
                        break
                    else:
                        with open(os.path.join(arg_csv_path,"battery_start_tempreture.csv"),'ab') as write_file:
                            csv_writer = csv.writer(write_file)
                            csv_writer.writerow([item,row[1]])


def walk(path):
    for sub in os.listdir(path):
        sub_path = os.path.join(path, sub)

        if os.path.isdir(sub_path):
            walk(sub_path)
        else:
            if sub_path.endswith('.csv'):
                os.remove(sub_path)
            elif sub_path.endswith('.log'):
                log2csv(sub_path)
            else:
                # unknown files
                pass
 
if __name__ == "__main__":
    cwdir = os.getcwd()

    walk(cwdir)