import requests
import redis
import time
import math


def send_msg(uid, peer_uid, num):
	for i in range(0, num):
		uid = uid
		peer_uid = 100001+i
		text = "发送消息{}".format(i)
		print(text)
		url = "https://testservice.hnyapu.cn/api/v2/message/send?uid={}".format(uid)
		bd_json = {
		  "content": {
		    "text_content": {
		      "content": text,
		      "highlight_content": "",
		      "highlights": [],
		      "leading": [],
		      "url": ""
		    },
		    "tips": ""
		  },
		  "msg_from_busi": "",
		  "peer_id": peer_uid,
		  "seq_id": 1636963350469,
		  "type": 1,
		  "yd_token": ""
		}
		rp = requests.post(url=url, json=bd_json)
		print(rp.content.decode())

def send_heartbeat():
	# 发送心跳
	with open('/Users/michael/Downloads/infos1.txt', 'r') as f:
		r = f.readlines()
		for i in r:
			# print(i.replace('\n', ''))
			url = 'https://testservice.localmeet.cn/api/daily/keepalive?uid={}&mod=1'.format(i.replace('\n', ''))
			rp = requests.get(url=url)
			print(rp.content.decode())

def add_online_list(uid, num):
	# 上线通知插入数据
	rd = redis.Redis(host='10.100.130.46', password='root', port=6379, db=0)
	time_stru = int(time.time())
	map = {}
	with open('/Users/michael/Downloads/infos1.txt', 'r') as f:
		read = f.readlines()
	for i in range(num):
		per_uid = read[1+i].strip()
		map[str(per_uid)] = str(time_stru)
	res = rd.zadd('pcc:uol:210820:{}'.format(uid), map)
	print(res)
	z_count = rd.zcard('pcc:uol:210820:{}'.format(uid))
	print(z_count)


def add_unactive_user_appointment():
	# 给一键搭讪不活跃池子写入数据
	rd = redis.Redis(host='10.100.130.46', password='root', port=6379, db=0)
	today_time = time.strftime('%Y%m%d', time.localtime())
	unactive_key = 'ugr:210723:naau:{}:{}'.format(today_time, 0)
	print(unactive_key)
	num = 100
	for i in range(1000400, 1000400+num):
		rd.sadd(unactive_key, i)


if __name__ == '__main__':
	# send_msg(1061705, 111111, 1)
	while True:
		send_heartbeat()
		time.sleep(2)
		print('#############')
	# print(94*0.2+100*0.2+86*0.3+100*0.3)
	# add_unactive_user_appointment()
	# print(10107985%16)

	


	


