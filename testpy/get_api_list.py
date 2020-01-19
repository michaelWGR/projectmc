import requests
import json
import os

def get_apidoc_cookie():
    URL = 'http://apidoc.61info.com/Guest/login'
    data = {
        'loginName': 'wangguirong',
        'loginPassword': 'de5409ae1597a6f47bd4826cf92c4225'
    }
    response = requests.post(url=URL, data=data)
    rp_dict = json.loads(response.content)
    cookie = 'JSESSIONID={}'.format(rp_dict['JSESSIONID'])
    return cookie

def get_api_list(project_id, group_id, file_path):
    cookie = get_apidoc_cookie()

    url = 'http://apidoc.61info.com/Api/getAllApiList'
    data = {
        'projectID': project_id,
        'groupID': group_id,
        'orderBy': 3,
        'asc': 0,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': cookie,
    }

    response = requests.post(url=url, data=data, headers=headers)
    dict_rp = json.loads(response.content)

    if os.path.exists(file_path):
        os.remove(file_path)

    write_madown('| id | 接口名称 | 接口地址 | 描述 | 状态 |\n', file_path)
    write_madown('| -- | -- | -- | -- | -- |\n', file_path)

    count = 0
    for api in dict_rp['apiList']:
        count += 1
        data = '| {} | {} | {} | | |\n'.format(count, api['apiName'], api['apiURI'])
        write_madown(data, file_path)

    print(count)

def write_madown(data, path):
    apiFile_path = path
    # print(apiFile_path)
    with open(apiFile_path, 'a+') as af:
        af.write(data)

def read_madown(path=r'E:\michael\schedule\liveApi_test.md'):
    with open(path, 'rb') as af:
        data = af.readlines()
        list_num = [str(i) for i in range(1, 176)]
        list_id = []
        for d in data:
            str_d = d.decode().strip()
            if '|' in str_d:
                list_d = str_d.split('|')
                list_id.append(list_d[1].strip())
        for n in list_num:
            if n in list_id:
                print(n)
            else:
                print('###### {}'.format(n))


def main():
    project_id = 1
    group_id = -1
    file_path = os.path.join(r'E:\michael\schedule', 'api.md')
    # cookie = 'JSESSIONID=644B5D0093E4AF0D8A719B6B1EE5B682'
    get_api_list(project_id, group_id, file_path)

    # write_madown(1)
    # read_madown()

if __name__ == '__main__':
    main()