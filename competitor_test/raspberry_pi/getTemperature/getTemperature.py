#!-*-coding:utf8-*--
import argparse
import os
import datetime
import time
from w1thermsensor import W1ThermSensor

SENSORS_MAP = {
	'031633c2aaff': '1A',
	'04163374ccff': '1B',
	'031633926eff': '2A',
	'031623c2deff': '2B',
	'04163372d9ff': '3A',
	'031633bfdeff': '3B',
	'031633bfadff': '4A',
	'0316339341ff': '4B',
	'031633c324ff': '5A',
	'031633c305ff': '5B',
	'031623c24bff': '6A',
	'031633c235ff': '6B'
}
TIME_FORMAT = '%Y-%m-%d_%H:%M:%S'

sensors = [x for x in W1ThermSensor.get_available_sensors()]
sensors_result = {}

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', help=u'指定测量温度的时间, 单位为分钟', type=int)
parser.add_argument('-s', '--store-path', help=u'结果存储路径，csv格式。当指定-t参数时才有效', type=str)
args = parser.parse_args()

def init():
	for sensor in sensors:
		sensors_result[sensor.id] = []

def getTemperature():
	for sensor in sensors:
		_time = datetime.datetime.now().strftime(TIME_FORMAT)
		tem = sensor.get_temperature()
		sensors_result[sensor.id].append((_time, tem))
		print(SENSORS_MAP[sensor.id], _time, tem)
	print('\n')

def write2file(path, sensor_id):
	content = 'time,' + SENSORS_MAP[sensor_id] + '\n'
	with open(path, 'w') as f:
		for item in sensors_result[sensor_id]:
			content += item[0] + ',' + str(item[1]) + '\n'
		f.write(content)

def main():
	if args.time is None:
		while True:
			for sensor in sensors:
				print(SENSORS_MAP[sensor.id], datetime.datetime.now().strftime(TIME_FORMAT), sensor.get_temperature())
			print('\n')
	else:
		init()
		run_time = args.time * 60
		start_time = datetime.datetime.now()

		while  (datetime.datetime.now() - start_time).total_seconds() <= run_time:
			getTemperature()
			time.sleep(5)

		for sensor in sensors:
			if args.store_path is None:
				write2file(start_time.strftime(TIME_FORMAT) + '_' + SENSORS_MAP[sensor.id] + '.csv', sensor.id)
			else:
				write2file(args.store_path + '_' + SENSORS_MAP[sensor.id] + '.csv', sensor.id)

if __name__ == '__main__':
	main()
