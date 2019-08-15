# -*- coding: utf-8 -*-
import requests
import re

#是否有版权你自己判断，小傻瓜，我看到的都是有版权的
#这是一首歌的url地址，需要hash和album_id
# url2 = 'http://www.kugou.com/song/#hash=AC84D9C9A823A9E52F5BF63397A23411&album_id=183876'

# 通过歌手id爬取音乐
def get_music_msg(singer_id):
    url= 'http://www.kugou.com/yy/singer/home/{}.html'.format(singer_id)

    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_2) AppleWebKit/537.36(KHTML,like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    response = requests.post(url,headers= headers)
    pattern = re.compile(r'class="cb\ssong_hid"\svalue="(.*)"\s/>')
    song_msg = re.findall(pattern,response.content)
    if len(song_msg)==0 :
        return
    for item in song_msg:
        pattern_msg = re.compile(r'(.*)\s-\s(.*)\|(.*)\|(\d+)')
        result = re.match(pattern_msg, item)
        singer_name = result.group(1)
        song_name = result.group(2)
        hash_id = result.group(3)
        album_id = result.group(4)
        print '{} {} {} {}'.format(hash_id,album_id,song_name,singer_name)

def main():
    #爬取歌手ID为1-99
    for i in range(100,120):
        get_music_msg(i)

if __name__ == '__main__':
    main()