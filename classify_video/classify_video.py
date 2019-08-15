# -*- coding: utf-8 -*-
import os
import shutil

hero_map = {"关羽" : "guanyu",  "李白" : "libai",  "白起" : "baiqi",  "刘备" : "liubei",  "吕布" : "lvbu",  "张良" : "zhangliang",  "张飞" : "zhangfei",  "百里守约" : "bailishouyue",  "元歌" : "yuange",  "干将莫邪" : "ganjiangmoxie",  "雅典娜" : "yadiannuo",  "老夫子" : "laofuzi",  "米莱狄" : "milaidi",  "百里玄策" : "bailixuance",  "铠" : "kai",  "甄姬" : "zhenji",  "女娲" : "nvwa",  "达摩" : "damo",  "鬼谷子" : "guiguzi",  "成吉思汗" : "chengjisihan",  "黄忠" : "huangzhong",  "橘右京" : "juyoujing",  "李元芳" : "liyuanfang",  "武则天" : "wuzetian",  "韩信" : "hanxin",  "王昭君" : "wangzhaojun",  "梦奇" : "mengqi",  "杨玉环" : "yangyuhuan",  "赵云" : "zhaoyun",  "明世隐" : "mingshiyin",  "后羿" : "houyi",  "裴擒虎" : "peiqinhu",  "典韦" : "dianwei",  "夏侯惇" : "xiahoudun",  "貂蝉" : "diaochan",  "周瑜" : "zhouyu",  "安琪拉" : "anqila",  "廉颇" : "lianpo",  "大乔" : "daqiao",  "娜可露露" : "nuokelulu",  "花木兰" : "huamulan",  "太乙真人" : "taiyizhenren",  "公孙离" : "gongsunli",  "弈星" : "yixing",  "苏烈" : "sulie",  "鲁班七号" : "lubanqihao",  "嬴政" : "yingzheng",  "亚瑟" : "yase",  "高渐离" : "gaojianli",  "项羽" : "xiangyu",  "牛魔" : "niumo",  "曹操" : "caocao",  "哪吒" : "nazha",  "刘禅" : "liushan",  "东皇太一" : "donghuangtaiyi",  "孙策" : "sunce",  "孙膑" : "sunbin",  "蔡文姬" : "caiwenji",  "兰陵王" : "lanlingwang",  "孙尚香" : "sunshangxiang",  "虞姬" : "yuji",  "不知火舞" : "buzhihuowu",  "芈月" : "mieyue",  "孙悟空" : "sunwukong",  "庄周" : "zhuangzhou",  "马可波罗" : "makeboluo",  "宫本武藏" : "gongbenwucang",  "狄仁杰" : "direnjie",  "阿轲" : "ake",  "妲己" : "daji",  "露娜" : "lunuo",  "杨戬" : "yangjian",  "诸葛亮" : "zhugeliang",  "程咬金" : "chengyaojin",  "狂铁" : "kuangtie",  "刘邦" : "liubang",  "扁鹊" : "bianque",  "小乔" : "xiaoqiao",  "钟无艳" : "zhongwuyan",  "钟馗" : "zhongkui",  "姜子牙" : "jiangziya",  "墨子" : "mozi",
            }



def readDir(dir_path):
    all_files = []
    if dir_path[-1] == os.sep:
        print u'文件夹路径末尾不能有{}'.format(os.sep)
        return

    if os.path.isdir(dir_path):
        filelist = os.listdir(dir_path)

        for f in filelist:
            f = os.path.join(dir_path,f)

            if os.path.isdir(f):
                sub_files = readDir(f)
                all_files = sub_files + all_files
            elif f.endswith('.mp4') or f.endswith('.flv') or f.endswith('.mkv'):
                all_files.append(f)

        return all_files
    else:
        return 'Erro no dir'


def main():
    video_files = '/Volumes/I/video/9'

    video_path = readDir(video_files)
    # count = 0
    # for _ in video_path:
    #     count += 1
    # print count
    for hero in hero_map:
        hero_dir = os.path.join(video_files,hero_map[hero])
        if not os.path.exists(hero_dir):
            os.mkdir(hero_dir)

        for p in video_path:

            if hero in p:
                if not os.path.exists(p):
                    continue

                dirs, files = os.path.split(p)
                new_video_path = os.path.join(hero_dir,files)
                print new_video_path
                shutil.move(p,new_video_path)

    print 'finished!!'

if __name__ == '__main__':
    main()