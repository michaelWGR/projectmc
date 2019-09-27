import requests
import json
from math import radians, cos, sin, asin, sqrt

_KEY1 = '619ed12d1faba843409f7e4733b69374'
_KEY2 = 'a7a748325a547459c5611ea4449e01ba'
_KEY3 = '36485fd9cf9d4865138d746840a6dba5'
_KEY4 = '29e36d6ceb83210d60c240b20ff4491e'

def get_location(address, city, key=_KEY1):
    '''
    获取到指定坐标的经纬度
    :param key: 高德Key
    :param address: 结构化地址信息
    :param city: 指定查询的城市,指定城市的中文（如北京）、指定城市的中文全拼（beijing）、citycode（010）、adcode（110000）
    :return: 坐标
    '''
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'key': key,
        'address': address,
        'city': city
    }

    rp = requests.get(url=url, params=params)
    rp_dict = json.loads(rp.content)
    print(rp_dict)
    location = rp_dict['geocodes'][0]['location']

    return location

def get_regeo(location, radius=10, key=_KEY1, roadlevel=0, extensions='all'):
    '''
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
                if i['name']:
                    traffic_list.append(i['name'])
                    # print(i['name'])
        else:
            break
    return traffic_list

def geodistance(lng1,lat1,lng2,lat2):
    EARTH_REDIUS = 6371
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    dis=2*asin(sqrt(a))*EARTH_REDIUS*1000
    return dis


def main():
    key = _KEY4
    address = '广州市天河区棠下二社涌边一横巷69天辉商业大厦'
    city = '广州'
    print(key)
    lo = get_location(key, address, city)
    # if lo != '':
    #     lng = float(lo.split(',')[0])
    #     lat = float(lo.split(',')[1])
    #     location = {'lng': lng, 'lat': lat}
    #     print(location)
    # print(lo)
    # get_regeo(lo, key=key)

    # address = '广州市黄埔大道西120号高志大厦'
    # city = '广州'
    # lo = get_location(key, address, city)
    # print(lo)
    # get_regeo(lo)
    # tl = get_around_place(lo, '1000', key=key)
    # for i in tl:
    #     print(i)

if __name__ == '__main__':
    main()
