import requests
import json

_KEY1 = '619ed12d1faba843409f7e4733b69374'
_KEY2 = 'a7a748325a547459c5611ea4449e01ba'
_KEY3 = '36485fd9cf9d4865138d746840a6dba5'

def get_location(key, address, city):
    '''
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
    location = rp_dict['geocodes'][0]['location']
    return location

def get_regeo(location, radius=100, key=_KEY1, roadlevel=0, extensions='all'):
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

def get_around_place(location, radius, offset='20', page='1', keywords='地铁公交', types='150500|150501|150600|150700|150702', extensions='all', key=_KEY1):
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
    print(rp.content.decode('utf-8'))
    rp_dict = json.loads(rp.content)
    pois = rp_dict['pois']

    # print(rp_dict['sug_address'])
    # for i in rp_dict:
    #     print('{}: {}'.format(i, rp_dict[i]))
    print(pois)
    for i in pois:
        print(i)

def main():
    key = _KEY1
    address = '广州市天河区棠下二社涌边一横巷69天辉商业大厦'
    city = '广州'
    lo = get_location(key, address, city)
    print(lo)
    get_regeo('113.383478,23.131367')

    # address = '广州市黄埔大道西120号高志大厦'
    # city = '广州'
    # lo = get_location(key, address, city)
    # print(lo)
    # get_regeo(lo)
    # get_around_place('113.383479,23.131373', '5000', page='1', types='150700|150701|150702')

if __name__ == '__main__':
    main()
