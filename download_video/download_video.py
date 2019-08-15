#-*- coding:utf-8 -*-

import os
import csv
import subprocess

def main():
	file_path = '4-2.csv'
	file_name = os.path.basename(file_path).split('.')[0]
	
	video_list = []
	with open(file_path, 'rU') as r_f:
		reader = csv.reader(r_f)
		for line in reader:
			video_list.append(line[0])

	for i in range(len(video_list)):
		# print video_list[i]
		cmd = ['youtube-dl',video_list[i]]
		child = subprocess.Popen(cmd)
		child.wait()
		# return 


if __name__ == '__main__':
	main()