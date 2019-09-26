import requests
import json

_key1 = 'aUYeI7XuUKMwSUv5jx7P2aFG4XAzvVxZ'

def get_code(address, city, ak=_key1, output='json'):
    url = 'http://api.map.baidu.com/geocoding/v3'
    params = {
        'address': address,
        'city': city,
        'ak': ak,
        'output': output
    }
    rp = requests.get(url=url, params=params)
    rp_dict = json.loads(rp.content)
    print(rp_dict)




def main():
    address = '广州市天河区棠下二社涌边一横巷69天辉商业大厦'
    city = '广州'
    get_code(address, city)
    
if __name__ == '__main__':
    main()
