import requests
import json
import os

url_list = []


def get_404_api(url):
    try:
        rp = requests.get(url)
        rp_dic = json.loads(rp.content)
        dm_error = str(rp_dic['dm_error'])
        if dm_error == '404':
            return True
        print(dm_error)
        return False
    except Exception as e:
        print(e)
        return True


def read_file(path):
    with open(path, 'r') as f:
        for ln in f.readlines():
            line = ln.strip()
            if line != '' and 'http' in line:
                url_list.append(line)


def patch_request(path, save_path='./404_api.txt'):
    read_file(path)
    for url in url_list:
        bl = get_404_api(url)
        if bl:
            write_file(save_path, url)
            print(url)


def write_file(path, url):
    with open(path, 'a') as fw:
        fw.write(url)
        fw.write('\n')


def get_api(path):
    with open(path, 'r') as fr:
        for ln in fr.readlines():
            # print(ln)
            print(ln.split('"'))
            for s in ln.split('"'):
                if '/' in s:
                    s = s.replace('App', 'https://servicelp.xinjuhn.com')
                    write_file('./all_api.txt', s)
                    break


if __name__ == '__main__':
    # t = get_404_api('https://servicelp.xinjuhn.com/api/resource/commond')
    # print(t)
    # read_file('./apitest.txt')
    # print(url_list)
    patch_request('./apitest.txt')
    # get_api('./HttpHost.java')
