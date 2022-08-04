# 1. 无忧代理  : http://www.data5u.com/
# 2. 快代理   : https://www.kuaidaili.com/
# 3. 小舒代理  : http://www.xsdaili.com/
# 4. 西刺代理  : http://www.xicidaili.com/
# 5. 89免费代理: http://www.89ip.cn/
# 代码来源：https://www.cnblogs.com/lizm166/p/9480318.html
from bs4 import BeautifulSoup
from random import choice
import requests
import re
import csv
import os


def get_html(url, open_proxy=False, ip_proxies=None):
    """
    获取页面的html文件
    :param url: 待获取页面的链接
    :param open_proxy: 是否开启代理，默认为False
    :param ip_proxies: 若开启，代理地址
    :return:
    """
    try:
        pattern = re.compile(r'//(.*?)/')
        host_url = pattern.findall(url)[0]
        headers = {
            "Host": host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        if open_proxy:  # 判断是否开启代理
            proxies = {"http": "http://" + ip_proxies, }  # 设置代理，例如{"http": "http://103.109.58.242:8080", }
            res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        else:
            res = requests.get(url, headers=headers, timeout=5)
        res.encoding = res.apparent_encoding  # 自动确定html编码
        print("Html页面获取成功 " + url)
        return res.text  # 只返回页面的源码
    except Exception as e:
        print("Html页面获取失败 " + url)
        print(e)


def save_ip(data, save_path):
    """
    将获取的ip信息保存到文件中
    :param data: 代理ip数据，数据类型为列表
    :param save_path: 代理ip保存路径
    :return:
    """
    try:
        print("总共获取 " + str(len(data)) + " 条数据")
        with open(save_path, "w") as f:
            for i in range(len(data)):
                writer = csv.writer(f)
                writer.writerow(data[i])
            print("文件保存成功")
    except Exception as e:
        print("文件保存失败！！！")
        print(e)


def get_89ip_free_ip(save_path, page=10, open_proxy=False, ip_proxies=None):
    """
    获取89免费代理的免费ip
    :param ip_proxies: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 代理ip保存路径
    :param open_proxy: 是否开启代理，默认为False
    :return:
    """
    ip_list_sum = []
    for i in range(page):  # 获取页数
        res_text = get_html("http://www.89ip.cn/index_" + str(i + 1) + ".html", open_proxy=open_proxy,
                            ip_proxies=ip_proxies)
        # 抓取错误页面，主动报异常
        if res_text.find("错误") != -1:  # 错误页面
            raise AttributeError('错误页面')
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("tbody")
        for tag in tags:
            ip_ths = tag.find_all("tr")
            for ip_th in ip_ths:
                ip_tds = ip_th.find_all("td")
                ip_list = []
                for ip_td in ip_tds:
                    ip_info = re.split(r'[\t\n ]', ip_td.get_text())  # 分割字符串
                    for j in range(len(ip_info)):
                        if ip_info[j] != "":
                            ip_list.append(ip_info[j])

                ip_list_sum.append(ip_list)
    save_ip(ip_list_sum, save_path)


def ip_test(ip, port):
    """
    验证单个代理ip是否可用
    :param ip: 待验证ip，例如：101.96.10.36
    :param port: 待验证端口，例如88
    :return:
    """
    http_url = "https://www.baidu.com"
    try:
        proxies = {"http": "http://" + ip + ':' + port}
        response = requests.get(http_url, proxies=proxies, timeout=2)
        return True
    except:
        print("invalid ip and port,cannot connect baidu")
        return False


def delete_ip(ip, save_path):
    """
    删除无效ip
    :param ip: 无效IP，例如 27.43.190.193
    :param save_path: ip保存的文件路径
    :return:
    """
    with open(save_path, 'r') as csv_r:
        reader = csv.reader(csv_r)
        csv_list = []
        for line in reader:
            csv_list.append(line)

    with open(save_path, 'w') as csv_w:
        writer = csv.writer(csv_w)
        for line in csv_list:
            if ip not in line:
                writer.writerow(line)
        print('delete ip:{}'.format(ip))


def get_proxies(save_path):
    """
    获取代理ip
    :param save_path: ip的保存路径
    :return: 返回代理dict，例如{'http': 'http://36.248.132.160:9999'}
    """
    if os.path.exists(save_path):
        with open(save_path, 'r') as f:
            reader = csv.reader(f)
            reader_list = []
            for l in reader:
                reader_list.append(l)  # 把读到的文件先写到列表内
        line = choice(reader_list)
        if len(line) > 0:  # 判断文件内是否有内容
            ip = line[0]
            port = line[1]
            if ip_test(ip, port):  # 判断IP是否可用
                proxies = {
                    'http': 'http://{0}:{1}'.format(ip, port),
                    # 'https': 'http://{0}:{1}'.format(ip, port)
                }
                return proxies
            else:
                delete_ip(ip, save_path)  # ip不可用，删除ip
                return get_proxies(save_path)  # 重新再获取一次代理
        else:
            get_89ip_free_ip(save_path, page=10)  # 文件内没有内容就重新请求写入
            return get_proxies(save_path)
    else:
        get_89ip_free_ip(save_path, page=10)  # 文件不存在就重新请求写入
        return get_proxies(save_path)


if __name__ == '__main__':
    # get_89ip_free_ip('./proxy.csv', page=1)
    y = ip_test('27.43.190.193', '9999')
    print(y)
    # delete_ip('36.249.52.30', './proxy.csv')
    ip = get_proxies('./proxy.csv')
    print(ip)
