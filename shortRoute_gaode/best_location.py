import requests
import json
from math import radians, cos, sin, asin, sqrt

_KEY1 = '619ed12d1faba843409f7e4733b69374'
_KEY2 = 'a7a748325a547459c5611ea4449e01ba'
_KEY3 = '36485fd9cf9d4865138d746840a6dba5'
_KEY4 = '29e36d6ceb83210d60c240b20ff4491e'

def get_location(address, city, key=_KEY1):
    '''
    获取到指定坐标的经纬度string(lng,lat)
    :param key: 高德Key
    :param address: 结构化地址信息
    :param city: 指定查询的城市,指定城市的中文（如北京）、指定城市的中文全拼（beijing）、citycode（010）、adcode（110000）
    :return: 坐标，例如113.376984,23.125229
    '''
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'key': key,
        'address': address,
        'city': city
    }

    rp = requests.get(url=url, params=params)
    rp_dict = json.loads(rp.content)
    location = rp_dict['geocodes'][0]['location']

    return location

def get_regeo(location, radius=10, roadlevel=0, extensions='all', key=_KEY1):
    '''
    通过经纬度获取地址
    :param location: 经纬度坐标
    :param radius: radius取值范围在0~3000，默认是1000。单位：米
    :param key: 高德Key
    :param roadlevel: 道路等级,以下内容需要 extensions 参数为 all 时才生效。可选值：0，1;当roadlevel=0时，显示所有道路;当roadlevel=1时，过滤非主干道路，仅输出主干道路数据
    :param extensions: 返回结果控制,extensions 参数默认取值是 base，也就是返回基本地址信息；extensions 参数取值为 all 时会返回基本地址信息、附近 POI 内容、道路信息以及道路交叉口信息。
    :return:
    '''
    url = 'https://restapi.amap.com/v3/geocode/regeo'
    params = {
        'location': location,
        'radius': radius,
        'key': key,
        'roadlevel': roadlevel,
        'extensions': extensions

    }
    rp = requests.get(url=url, params=params)
    # print(rp.content.decode('utf-8'))
    for i in json.loads(rp.content)['regeocode']['pois']:
        print(i)

def get_around_place(location, radius, offset='20', keywords='地铁|公交', types='150500|150501|150700|150701|150702', extensions='all', key=_KEY1):
    '''
    获取定圆心和半径内的周边信息
    :param location: 中心点坐标，经度和纬度
    :param radius: 查询半径，取值范围:0-50000。规则：大于50000按默认值，单位：米
    :param offset: 每页记录数据
    :param keywords: 查询关键字， 多个关键字用“|”分割
    :param types: 查询POI类型
    :param extensions: base:返回基本信息；all：返回全部信息
    :param key:
    :return: 返回信息列表，例如[{'name': '员村山顶(东行)(公交站)', 'location': '113.357903,23.124016'},{'name': '员村山顶站(临时站)(公交站)', 'location': '113.357819,23.124031'}]
    '''
    traffic_list = []
    page = 1
    while True:
        url = 'https://restapi.amap.com/v3/place/around'
        params = {
            'key': key,
            'location': location,
            'keywords': keywords,
            'types': types,
            'radius': radius,
            'offset': offset,
            'page': page,
            'extensions': extensions
        }
        rp = requests.get(url=url, params=params)
        rp_dict = json.loads(rp.content)
        pois = rp_dict['pois']
        print(pois)
        if len(pois) != 0:
            page += 1
            for i in pois:
                traffic_info_dict = {}
                if i['name'] and i['location']:
                    traffic_info_dict['name'] = i['name']
                    traffic_info_dict['location'] = i['location']
                    traffic_list.append(traffic_info_dict)
                    # print(i['name'])
        else:
            break
    return traffic_list

# def geodistance(location1, location2):      # 通过球半径计算，暂时不用
#     #计算两个经纬度距离/米(float)
#     if location1 != '' and location2 != '':
#         lng1 = float(location1.split(',')[0])
#         lat1 = float(location1.split(',')[1])
#         lng2 = float(location2.split(',')[0])
#         lat2 = float(location2.split(',')[1])
#     else:
#         return
#
#     EARTH_REDIUS = 6371
#     lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
#     dlon=lng2-lng1
#     dlat=lat2-lat1
#     a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     dis=2*asin(sqrt(a))*EARTH_REDIUS*1000
#     return dis

def get_centre_point(location1, location2):
    # 获取两点间的圆心,返回string(lng,lat)，例如113.357201,23.124350
    if location1 != '' and location2 != '':
        lng1 = float(location1.split(',')[0])
        lat1 = float(location1.split(',')[1])
        lng2 = float(location2.split(',')[0])
        lat2 = float(location2.split(',')[1])
    else:
        return

    lng = (lng1+lng2)/2
    lat = (lat1+lat2)/2
    centre_location = '{},{}'.format(lng, lat)
    return centre_location

def get_distance(origins, destination, type=0, key=_KEY1):      # 通过请求获取
    '''
    计算两点距离/米(int)
    :param origins:出发点
    :param destination:目的地
    :param type: 0：直线距离,1：驾车导航距离（仅支持国内坐标）
    :param key:
    :return: 3814
    '''
    url = 'https://restapi.amap.com/v3/distance'
    params = {
        'origins': origins,
        'destination': destination,
        'type': type,
        'key': key
    }
    rp = requests.get(url=url, params=params)
    rp_dict = json.loads(rp.content)
    distance = rp_dict['results'][0]['distance']
    return int(distance)

def get_transit_direction(origin, destination, city='广州', cityd='广州', extensions='base', strategy=0, nightflag=0, date=None, time='8:30', key=_KEY1):
    '''
    获取到起点到终点的路线的平均值
    :param origin: 出发点（经度，纬度）
    :param destination: 目的地（经度，纬度）
    :param city: 城市/跨城规划时的起点城市
    :param cityd: 跨城公交规划时的终点城市
    :param extensions: base:返回基本信息；all：返回全部信息
    :param strategy: 可选值：0：最快捷模式;1：最经济模式;2：最少换乘模式;3：最少步行模式;5：不乘地铁模式
    :param nightflag: 可选值：0：不计算夜班车;1：计算夜班车
    :param date: 出发日期，格式示例：date=2014-3-19
    :param time: 出发时间，格式示例：time=22:34
    :param key:
    :return: 平均值信息的字典,例如{'per_cost': 2.0, 'per_duration': 1509.6, 'per_walking_distance': 585.6, 'per_distance': 2509.2}
    '''
    transit_direction = {}
    url = 'https://restapi.amap.com/v3/direction/transit/integrated'
    params = {
        'origin': origin,
        'destination': destination,
        'city': city,
        'cityd': cityd,
        'extensions': extensions,
        'strategy': strategy,
        'nightflag': nightflag,
        'date': date,
        'time': time,
        'key': key
    }
    rp = requests.get(url=url, params=params)
    rp_dict = json.loads(rp.content)
    print(rp_dict)
    j = json.dumps(rp_dict)
    print(j)
    if rp_dict['route']['transits']:
        cost_list = []
        duration_list = []
        walking_distance_list = []
        distance_list = []
        transits_list = rp_dict['route']['transits']

        try:
            for t in transits_list:
                if t != {}:
                    cost_list.append(float(t['cost']))
                    duration_list.append(float(t['duration']))
                    walking_distance_list.append(float(t['walking_distance']))
                    distance_list.append(float(t['distance']))
                    # print(t)
            per_cost = sum(cost_list) / len(cost_list)
            per_duration = sum(duration_list) / len(duration_list)
            per_walking_distance = sum(walking_distance_list) / len(walking_distance_list)
            per_distance = sum(distance_list) / len(distance_list)

            transit_direction['per_cost'] = per_cost
            transit_direction['per_duration'] = per_duration
            transit_direction['per_walking_distance'] = per_walking_distance
            transit_direction['per_distance'] = per_distance

            return transit_direction

        except Exception as e:
            print(e)

    else:
        print("{rp_dict['route']['transits']} is error")
        return transit_direction

def aggregate_target_info(key=_KEY1, *location, **traffic_dict):
    '''
    集成一个交通站点到各个终点的目标信息
    :param key:
    :param location: 各个终点站的坐标，例如'113.357903,23.124016', '114.357903,24.124016'
    :param traffic_dict: 一个交通站点的信息，例如{'name': '员村山顶(东行)(公交站)', 'location': '113.357903,23.124016'}
    :return: 目标交通站的通勤时间信息，例如{name, location, total_per_duration, ......,detail: [{per_duration, ....}, {per_duration, ....}], around_place: {...}}
    '''
    target_info_dict = {}
    traffic_location = traffic_dict['location']
    # print(traffic_dict)
    # print(traffic_location)

    detail = []
    per_cost_list = []
    per_duration_list = []
    per_walking_distance_list = []
    per_distance_list = []
    for lo in location:
        d = get_transit_direction(traffic_location, lo, key=key)
        if d != {}:
            detail.append(d)
            per_cost_list.append(d['per_cost'])
            per_duration_list.append(d['per_duration'])
            per_walking_distance_list.append(d['per_walking_distance'])
            per_distance_list.append(d['per_distance'])

    total_per_cost = sum(per_cost_list)/len(per_cost_list)
    total_per_duration = sum(per_duration_list)/len(per_duration_list)
    total_per_walking_distance = sum(per_walking_distance_list)/len(per_walking_distance_list)
    total_per_distance = sum(per_distance_list)/len(per_distance_list)

    # print(detail)

    target_info_dict['name'] = traffic_dict['name']
    target_info_dict['location'] = traffic_dict['location']
    target_info_dict['total_per_cost'] = total_per_cost
    target_info_dict['total_per_duration'] = total_per_duration
    target_info_dict['total_per_walking_distance'] = total_per_walking_distance
    target_info_dict['total_per_distance'] = total_per_distance
    target_info_dict['detail'] = detail

    print(target_info_dict)
    return target_info_dict

def quick_sort(array, dict_key=None):
    '''
    #快排算法，从低到高排序
    :param array: 列表
    :param dict_key: 列表内为dict的话，设置要排序的key的值，用‘.’符号分开，例如detail.0.per_cost
    :return: 排好序的列表
    '''
    if len(array) <= 1:
        return array
    if dict_key != None:
        dict_key_list = dict_key.split('.')
        less = []
        greater = []
        base = array.pop()
        base_value = base
        for k in dict_key_list:
            if k.isdigit():
                k = int(k)
            base_value = base_value[k]
        for i in array:
            i_value = i
            for k in dict_key_list:
                if k.isdigit():
                    k = int(k)
                i_value = i_value[k]

            if i_value < base_value:
                less.append(i)
            else:
                greater.append(i)

        return quick_sort(less, dict_key=dict_key) + [base] + quick_sort(greater, dict_key=dict_key)

    else:
        less = []
        greater = []
        base = array.pop()
        for i in array:
            if i < base:
                less.append(i)
            else:
                greater.append(i)

        return quick_sort(less) + [base] + quick_sort(greater)


def main():
    key = _KEY1
    address = '广州市天河区棠下二社涌边一横巷69天辉商业大厦'
    city = '广州'
    lo1 = get_location(address, city, key=key)
    get_regeo(lo1, key=key)

    address = '广州市黄埔大道西120号高志大厦'
    city = '广州'
    lo2 = get_location(address, city, key=key)
    get_regeo(lo2, key=key)

    distance = get_distance(lo1, lo2)
    print(distance)
    circle_radius = int(distance/2)+500
    print(circle_radius)
    centre_location = get_centre_point(lo1, lo2)


    # tl = get_around_place(centre_location, circle_radius, key=key)
    #
    # best_location_list = []
    # count = 0
    # for i in tl:
    #     count += 1
    #     target_info_dict = aggregate_target_info(key, lo1, lo2, **i)
    #     if target_info_dict:
    #         best_location_list.append(target_info_dict)
    #
    # print(count)
    # print('######################################################')
    #
    # sort_list = quick_sort(best_location_list, dict_key='total_per_duration')
    # for s in sort_list:
    #     print(s)


    d = get_transit_direction('113.357903,23.124016', lo2, extensions='all')
    print(d)


    # test_traffic_dict = {'name': '员村山顶(东行)(公交站)', 'location': '113.357903,23.124016'}
    # aggregate_target_info(_KEY1, lo1, lo2, **test_traffic_dict)

if __name__ == '__main__':
    main()
    # print(float('2.0'))
    # TODO:公交的班车间隔时间，地点的周边设施范围800m,公寓、超市，站点的公交

    # d = {'name': '员村山顶(东行)(公交站)', 'location': '113.357903,23.124016', 'total_per_cost': 2.0, 'total_per_duration': 1567.0, 'total_per_walking_distance': 661.1, 'total_per_distance': 3121.7, 'detail': [{'per_cost': 2.0, 'per_duration': 1624.4, 'per_walking_distance': 736.6, 'per_distance': 3734.2}, {'per_cost': 2.0, 'per_duration': 1509.6, 'per_walking_distance': 585.6, 'per_distance': 2509.2}]}
    # # key = 'detail.0.per_cost'
    # key = 'location'
    # key_list = key.split('.')
    # print(key_list)
    # for k in key_list:
    #     if k.isdigit():
    #         k = int(k)
    #     d = d[k]
    # print(d)