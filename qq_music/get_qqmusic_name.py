# -*- coding: utf-8 -*-

import requests
import json

#这是一首歌的url样例
#url = 'https://y.qq.com/n/yqq/song/0039MnYb0qxYhV.html'

# 获取歌手的mid
def get_singermid():
    url = 'https://c.y.qq.com/v8/fcg-bin/v8.fcg'
    singermid = []
    # 可以设置多页的歌手循环
    for num in range(1,2):

        data = {
        'channel': 'singer',
        'page': 'list',
        'key': 'all_all_all',
        'pagesize': '100',
        'pagenum': str(num),
        'format': 'jsonp',
        }

        response = requests.post(url,data= data)
        singer_json = response.content
        singer_dict = json.loads(singer_json,encoding='utf-8')
        singer_list = singer_dict['data']['list']
        for item in singer_list:
            singermid.append(item['Fsinger_mid'])
    return singermid

# 通过歌手的mid，获取歌曲信息
def get_song_by_singer(singermid):
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg'

    data= {
        'singermid': singermid,
        'order': 'listen',
        'begin': '0',
        'num': '1',
    }
    response_total = requests.post(url,data=data)
    total_json = response_total.content
    total_dict = json.loads(total_json,encoding='utf-8')
    song_total = total_dict['data']['total']

    data_all = {
        'singermid': singermid,
        'order': 'listen',
        'begin': '0',
        'num': song_total,
    }

    response = requests.post(url, data=data_all)
    song_json = response.content
    song_dict = json.loads(song_json,encoding='utf-8')
    song_list = song_dict['data']['list']
    singer_name = song_dict['data']['singer_name']
    # song_msg = []
    for i in song_list:
        song_name = i['musicData']['songname']
        song_mid = i['musicData']['songmid']
        if int(i['Flisten_count1']) >= 100000000:
            song_copyright = 'yes'
            # item = copyright.decode('utf-8')
            # print copyright
            print u'{} {} {} {}'.format(song_mid,song_name,singer_name,song_copyright)
        else:
            song_copyright = 'no'
            # # item = copyright.decode('utf-8')
            # print copyright
            print u'{} {} {} {}'.format(song_mid, song_name, singer_name, song_copyright)


def main():
    singermid_list = get_singermid()
    for item in singermid_list:
        get_song_by_singer(item)

if __name__ == '__main__':
    main()