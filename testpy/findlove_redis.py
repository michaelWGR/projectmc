import redis


def connect_redis(host, port=6379, db=0):
    r = redis.Redis(host=host, port=port, db=db)
    return r


def add_phone_white_list(phone, code):
    r = connect_redis('10.100.130.102')
    phone_white_list_key = 'PHONE_LOGIN_WHITE_LIST'
    add = r.hset(name=phone_white_list_key, key=phone, value=code)
    print(add)


if __name__ == '__main__':
    add_phone_white_list('8612345678806', '123456')
