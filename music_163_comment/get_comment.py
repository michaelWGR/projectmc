# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import codecs
import re
import time
import multiprocessing

def get_html(id):
    headers = {
        "Host": "music.163.com",
        "Referer": "https://music.163.com/",
        "User-Agent": "Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_2) AppleWebKit/537.36(KHTML,like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }

    data = {
        "params": "dZiFjiJwwUmuTrJeDHIOVaGL+X7eiSL/qOJBSwqyc3EZwji5ovGg325SnYveFkFFYGU8D5ZVBByCBZrbxX9roUVOuqN+lA7bExK/30krGCyrvJxur6HI/GiT6sefMv4wnpvVxNeKFU36eJB2L4atjDpYCu/forfkGsvdSV6D5PXQq9CchNzZLCT1x9QxGERQ",
        "encSecKey": "268e5e8cb215e8e2ed592c4411d78b3dbf815b45077d05fc8f1906307796511dc7a69948057caf1ae59a1e5e38df9eef218c08ac7c6d0d20341dc3baea832da6b65a97fd36604069a8bf7fc7d385d68e24dfb45a22bb762817850fd07b745615f7fdba74d1d5e09761d7450993d7e3f368529751a104efd12b9e8bc0fbd5e1fb",
    }
    response = requests.post("https://music.163.com/m/song?id={}".format(id), headers=headers, data=data)
    html_text = response.content
    return html_text
def music_is_true(title_html):
    soup = BeautifulSoup(title_html, "html.parser")
    pattern = re.compile(r"\<title\>([^<>]*)\s\-\s([^<>]+)\s\-\s[^<>]+\s\-\s[^<>]+\<\/title\>")
    title = re.match(pattern, str(soup.title))
    if title == None:
        return False
    else:
        return True
def comment_is_true(id):
    json_text = get_json(id)
    json_dict = json.loads(json_text, encoding="utf-8")
    total = json_dict.get("total")
    if total == 0:
        return False
    else:
        return True
def get_music_title(title_html):
    soup = BeautifulSoup(title_html,"html.parser")
    pattern = re.compile(r"\<title\>([^<>]*)\s\-\s([^<>]+)\s\-\s[^<>]+\s\-\s[^<>]+\<\/title\>")
    title = re.match(pattern,str(soup.title))
    fuck = "歌曲名称：{}  歌手：{}".format(title.group(1),title.group(2))
    return fuck
def get_json(id):
    headers = {
        "Host": "music.163.com",
        "Referer": "https://music.163.com/",
        "User-Agent": "Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_2) AppleWebKit/537.36(KHTML,like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }

    data = {
        "params": "dZiFjiJwwUmuTrJeDHIOVaGL+X7eiSL/qOJBSwqyc3EZwji5ovGg325SnYveFkFFYGU8D5ZVBByCBZrbxX9roUVOuqN+lA7bExK/30krGCyrvJxur6HI/GiT6sefMv4wnpvVxNeKFU36eJB2L4atjDpYCu/forfkGsvdSV6D5PXQq9CchNzZLCT1x9QxGERQ",
        "encSecKey": "268e5e8cb215e8e2ed592c4411d78b3dbf815b45077d05fc8f1906307796511dc7a69948057caf1ae59a1e5e38df9eef218c08ac7c6d0d20341dc3baea832da6b65a97fd36604069a8bf7fc7d385d68e24dfb45a22bb762817850fd07b745615f7fdba74d1d5e09761d7450993d7e3f368529751a104efd12b9e8bc0fbd5e1fb",
    }

    r = requests.post("https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(id),
                      headers=headers, data=data)
    return r.content
def get_hotcomments(id,title_html):
    song_info = get_music_title(title_html).decode("utf-8")
    json_text = get_json(id)
    json_dict = json.loads(json_text, encoding="utf-8")
    hotcomments_list = []
    hotcomments_list.append(u"{} 歌曲ID：{}\n".format(song_info,id))
    hotcomments_list.append(u"置顶评论\n")
    hotcomments_list.append(u"评论内容\n")
    topcomments = json_dict.get("topComments")
    for j in topcomments:
        content = j.get("content")
        hotcomments_list.append(content+u"\n\n")
    hotcomments_list.append(u"热门评论\n")
    hotcomments_list.append(u"点赞总数 评论内容\n")
    total = json_dict.get("total")
    hotcomments = json_dict.get("hotComments")
    count = len(json_dict.get("hotComments"))

    for i in hotcomments:
        likecount = str(i.get("likedCount"))
        content = i.get("content")
        hotcomments_list.append(likecount + u" " + content + u"\n")
    hotcomments_list.append(u"comments total: {}   hotcomments count: {}\n".format(total, count))
    hotcomments_list.append(u"#########################################################################################################\n\n")
    return hotcomments_list

def save_to_text(id,title_html):
    f = codecs.open("comments.text", "a",encoding="utf-8")
    hotcomments = get_hotcomments(id,title_html)
    f.writelines(hotcomments)
    print u"保存成功"
    # for j in hotcomments:
    #     writer = csv.writer(f)
    #     writer.writerows(j)
def main():
    begin = time.time()
    # file = codecs.open("comments.text", "w", encoding="utf-8")
    # file.truncate()
    # file.close()
    begin_id = 91301
    num = 100000
    max_id = begin_id +num
    sum = 0
    miss = 0
    # pool = multiprocessing.Pool(processes=4)
    for song_id in range(begin_id,max_id):
        html_text = get_html(str(song_id))
        if music_is_true(html_text)==False:
            song_id = song_id + 1
            miss = miss+1
            print miss
        else:
            # pool.apply(save_to_text,(str(song_id),html_text))
            save_to_text(str(song_id),html_text)
            song_id = song_id + 1
            sum = sum + 1
    # pool.close()
    # pool.join()
    print u"获取评论歌曲数：{}".format(sum)
    end = time.time()
    print "get comments time :{}s".format(end-begin)
if __name__ == "__main__":
    main()