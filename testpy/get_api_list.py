import requests
import json
import os


def get_api_list(project_id, group_id, file_path, cookie):
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
    # print(dict_rp)

    # apiFile_path = os.path.join(r'E:\michael\schedule', 'api2.md')
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
    # project_id = 1
    # group_id = -1
    # file_path = os.path.join(r'E:\michael\schedule', 'api2.md')
    # cookie = 'JSESSIONID=76930315EC0AD2CEAB62A8E021BCA486'
    # get_api_list(project_id, group_id, file_path, cookie)

    # write_madown(1)
    read_madown()

if __name__ == '__main__':
    main()
