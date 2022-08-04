import redis
import time
import requests
import json


def write_redis():
    """
    写入上线通知
    """
    r = redis.Redis(host='10.100.130.19', port=6379)
    # print(r)
    # t = r.zscore(name='lm:uml:rlu:20200806_20200811-1552', value=100273)
    # print(t)
    # print(time.localtime())
    # print(time.strftime('%Y%m%d-%H%M', time.localtime()))

    mapping_u = {}
    r_key = 'lm:uml:rlu:20200806_{}'.format(time.strftime('%Y%m%d-%H%M', time.localtime()))
    strutime = int(time.time())
    print(r_key)
    uid_list = ['100705', '100304', '100297', '100284', '100718', '100690', '100716', '100265', '100702', '100736',
                '100732', '100420', '100268', '100362', '100739', '100297', '100284', '100626', '100723', '100541',
                '100714', '100713', '100292', '100729', '100732', '100304', '100297', '100348', '100362', '100737',
                '100734', '100285', '100658', '100273', '100730', '100731', '100734', '100735', '100736', '100738',
                '100739', '100305', '100306', '100307', '100308', '100309', '100310', '100311', '100312', '100313',
                '100314', '100315', '100316', '100317', '100318', '100319', '100320', '100321', '100322', '100323',
                '100324', '100325', '100326', '100327', '100328', '100329', '100330', '100331', '100332', '100333',
                '100334', '100335', '100336', '100337', '100338', '100339']
    # uid_list = ['100204', '101162', '101140', '100636', '100637', '101131', '100237', '100641',
    #             '100639', '100730', '100798', '102822', '102821', '102823', '102824', '102912',
    #             '102913', '100675', '102914', '102909', '100671', '100236']
    for u in uid_list[0:10]:
        key = '{}:LM84483'.format(u)
        mapping_u[key] = strutime
    print(len(mapping_u))
    rsp = r.zadd(name=r_key, mapping=mapping_u)
    print(rsp)

    # l = []
    # for i in range(30):
    #     t = 100310+i
    #     l.append(str(t))
    # print(l)


def write_actacp():
    """写入在线陪陪，为触发暗搭讪"""
    r = redis.Redis(host='10.100.130.19', port=6379)
    re_key = 'lm:ugr:actacp:20200817'
    uid_list = ['100904', '100367', '100751', '100862', '100306', '100305', '100301', '100298', '100824', '100641',
                '100273', '100704', '100703', '100673', '101152', '100637', '101145', '100698', '100279', '100281',
                '100984', '100983', '100982', '100973', '100986', '100985', '100984', '100983', '100982', '100972',
                '100971', '100329', '100282', '100367', '100751', '100862', '100306', '100289']
    strutime = int(time.time())
    map_id = {}
    for u in uid_list:
        map_id[u] = strutime
    rsp = r.zadd(name=re_key, mapping=map_id)
    print(rsp)


def del_str_redis():
    r = redis.Redis(host='10.100.130.19', port=6379)
    rp = r.delete(*r.keys(pattern='greet_peer_*'))
    print(rp)


def add_redis(redis_key, mapping):
    r = redis.Redis(host='10.100.130.19', port=6379)
    rsp = r.zadd(name=redis_key, mapping=mapping)
    print(rsp)


def write_female_queue():
    uid_list = ['100575', '100287', '100285', '100780', '100783', '100493', '100769']
    mapping = {}
    struct_time = int(time.time())
    for u in uid_list:
        mapping[u] = struct_time
    redis_key = 'sml:qfmvtsqueue:20200603'
    add_redis(redis_key, mapping)


def send_heard_beat():
    # uid_list = [100761, 100346, 100279, 100281, 100734, 100731, 100726, 100725, 100719, 100461,
    #             100575, 100287, 100285, 100236, 100780, 100783, 100273, 100270, 100493, 100769,
    #             100730, 100289, 100290, 100293]

    # uid_list = ['100204', '101162', '101140', '100636', '100637', '101131', '100237', '100641',
    #             '100639', '100730', '100798', '102822', '102821', '102823', '102824', '102912',
    #             '102913', '100675', '102914', '102909', '100671', '100236']
    female_uid_list = [100287,100751,188709,100975,201063,201062,201044,175770,175796,124908,
                        100264,175861,175877,100575,188694,175797,100637,100780,100236,100493,
                        100783,100635,200916,175901,188648,100273,100641,175855,175884,175996,
                        175844,175953,175945,175946,175911,100201,100709,175821,175867,118637,
                        110970,100281,126311,124946,120367,120368,120267,120268,120283]
    while True:
        for u in female_uid_list:
            url = 'http://test.cheesesuperman.com/api/daily/keepalive'
            params = {
                'uid': u
            }
            rp = requests.get(url=url, params=params)
            print(rp.content.decode())
        time.sleep(60)


def cal_t():
    s = 6 * 0.1 * 2500
    print(s)
    r = 70000 + 70000 + 70000 + 50000 + 17500 + 17500
    print(r)
    print(40 * 0.94 + 40)
    t = 5 + 5 - 6
    print(77 + 4)
    print(100641 % 100)
    print(18.8 + 564)
    print(1500000 + 50000)
    r = redis.Redis(host='10.100.130.19', port=6379)
    print(r)
    k_dict = r.hgetall(name='USER_AUTH_ENTRY_STATE')
    print(k_dict)
    id_list = []
    for k in k_dict:
        peer_id = k.decode()
        print(peer_id)
        id_list.append(peer_id)
    print(id_list)


def send_hello():
    r = redis.Redis(host='10.100.130.19', port=6379)
    print(r)
    k_dict = r.hgetall(name='USER_AUTH_ENTRY_STATE')
    print(k_dict)

    for k in k_dict:
        peer_id = k.decode()
        print(peer_id)
    # for i in range(1000):
    #     print(i)
    #     url = 'http://test.cheesesuperman.com/api/v2/message/send?uid=100698'
    #     rq_json = {
    #             'peer_id': i,
    #             'miss_sendrp_check': 1,
    #             'seq_id': 1600830472071,
    #             'type': 17,
    #             'gift_id': 0
    #             }
    #     rp = requests.post(url=url, json=rq_json)
    #     print(rp.content.decode())


def send_app_config(num):
    for i in range(100200, 102000+num):
        url = 'https://test.lexiuhuyu.com/api/app/config?uid={}&cv=LOVEMEET2.0.00_Android&cc=LM84483'.format(i)
        rp = requests.get(url=url)
        print(rp.content.decode())


def zadd_acp_online(num, uid):
    r = redis.Redis(host='10.100.130.19', port=6379)
    struct_time = int(time.time())
    acp_key = 'lm:uon:olineus:20210121:{}'.format(uid)
    map = {}
    for i in range(100201, 100201+num):
        map[i] = struct_time
    rt = r.zadd(acp_key, map)
    print(rt)

def zadd_acp_online_by_uid(online_uid_list, uid):
    r = redis.Redis(host='10.100.130.19', port=6379)
    struct_time = int(time.time())
    acp_key = 'lm:uon:olineus:20210121:{}'.format(uid)
    map = {}
    for u in online_uid_list:
        map[u] = struct_time
    rt = r.zadd(acp_key, map)
    print(rt)


def receive_message(peerid, nums):

    url = 'http://test.lexiuhuyu.com/api/v2/message/send?uid={}'

    json = {
        "content": {
            "audio_content": {
                "duration": 0,
                "localUrl": "",
                "url": ""
            },
            "extra_comment": {
                "text_list": [],
                "highlight_list": []
            },
            "finan_attr": {
                "earn": 0,
                "earn_text": "",
                "need_show_tips": 0,
                "tips": ""
            },
            "gift_content": {
                "combo_code": "",
                "gift_id": -1,
                "gift_name": "",
                "gold": -1,
                "intimacy_value": -1.0,
                "res_id": -1,
                "seq": -1,
                "sub_res": {
                    "bundle": 1
                },
                "gift_type": -1
            },
            "highlight": [],
            "image_content": {
                "height": 0,
                "localUrl": "",
                "url": "",
                "width": 0
            },
            "links": [],
            "text_image_content": {
                "content": "",
                "image": "",
                "link": "",
                "title": ""
            },
            "text_image_jump_content": {
                "content": "",
                "image": "",
                "link": "",
                "title": ""
            },
            "text_content": {
                "content": "测试一条",
                "highlight_content": "",
                "highlights": [],
                "leading": [],
                "url": ""
            },
            "tips": "",
            "tips_img": ""
        },
        "from": 3,
        "peer_id": peerid,
        "seq_id": 1616410704077,
        "type": 1
    }
    uid = 100201
    for i in range(nums):
        print(i)
        uid += 1
        rp = requests.post(url=url.format(uid), json=json)
        print(rp.content.decode())


def add_ban():
    import redis

    r = redis.Redis(host='10.100.130.39', port=6379, db=7)

    num=997010
    for i in range(50):
      num=num+i
      t = r.zadd('sakura_2021_alpha2:honor1:local_tyrant', {num: '183510533'})
      print(t)

def update_ol_list():
    import redis

    r = redis.Redis(host='10.100.130.19', port=6379, db=0)
    u_list = r.zrange('g:ol:uid:list', 0, 1000, withscores=False)
    print(u_list)
    mapping = {}
    time_stam = int(time.time()-50*60)
    for u in u_list:
        mapping[u.decode()] = time_stam
    t = r.zadd('g:ol:uid:list', mapping)
    print(t)

def add_ol_supple(num):
    """插入备用数据源"""
    import redis
    r = redis.Redis(host='10.100.130.19', port=6379, db=0)
    time_stam = int(time.time())
    mapping = {}

    for i in range(100200, 100200+num):
        mapping[i] = time_stam
    t = r.zadd('ol:supple:uid:list', mapping)
    print(t)


def send_heard_beat_by_ol_list():
    r = redis.Redis(host='10.100.130.19', port=6379, db=0)
    u_list = r.zrange('ol:supple:uid:list', 0, 1000, withscores=False)
    while True:
        for u in u_list:
            url = 'http://test.cheesesuperman.com/api/daily/keepalive'
            params = {
                'uid': u.decode()
            }
            rp = requests.get(url=url, params=params)
            print(rp.content.decode())
        time.sleep(60)

def update_uon_flimk():
    import redis

    r = redis.Redis(host='10.100.130.19', port=6379, db=0)
    u_list = r.zrange('uon:flimk', 0, 1000, withscores=False)
    print(u_list)
    mapping = {}
    time_stam = int(time.time()-50*60)
    for u in u_list:
        mapping[u.decode()] = time_stam
    t = r.zadd('uon:flimk', mapping)
    print(t)


if __name__ == '__main__':
    # cal_t()
    # write_redis()
    # send_heard_beat()
    # write_actacp()
    # del_str_redis()
    # write_female_queue()
    # send_hello()
    # zadd_acp_online(num=20, uid=100637)
    # send_app_config(1000)
    # zadd_acp_online_by_uid([100636,188645, 187928, 100634], 100635)
    # print(54061-49990-999
    # receive_message(100635, 20)
    # add_ban()
    # update_ol_list()
    # add_ol_supple(200)
    # send_heard_beat_by_ol_list()
    # update_uon_flimk()
    print((88+5200*10*2+52)*100/2500+1.04+1.04+1.76)
    print(185473.03/232)
    print(31580-26380)
    print(15799+199)
    print(20-20*0.06)


