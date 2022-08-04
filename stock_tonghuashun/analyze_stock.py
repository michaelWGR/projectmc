import requests
import time
import csv
import re
import json
import sqlite3
from random import choice, random
from bs4 import BeautifulSoup
from crawl_proxy import get_proxies

FAILURE_URL_LIST = []

class AnalyzeStock(object):
    def __init__(self):
        self.proxy_save = {}

    def downloader(self, url, num_retries=3):
        """
        请求url地址，获得返回值
        :param url: 请求的url
        :param num_retries: 重试次数
        :return: 返回请求后的body
        """
        if len(self.proxy_save) == 0:
            proxies = get_proxies('./proxy.csv')
            self.proxy_save = proxies
        else:
            proxies = self.proxy_save
        pattern = re.compile(r'//(.*?)/')
        host_url = pattern.findall(url)[0]
        headers_list = [{
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469,1533998895,1533998953; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998953; user=MDrAz9H9akQ6Ok5vbmU6NTAwOjQ2OTU0MjIzNDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQyMjM0OjE1MzM5OTkwNzU6OjoxNTMzOTk5MDYwOjg2NDAwOjA6MTZmOGFjOTgwMGNhMjFjZjRkMWZlMjk0NDQ4M2FhNDFkOmRlZmF1bHRfMjox; userid=459542234; u_name=%C0%CF%D1%FDjD; escapename=%25u8001%25u5996jD; ticket=7c92fb758f81dfa4399d0983f7ee5e53; v=Ajz6VIblS6HlDX_9PqmhBV0QDdH4NeBfYtn0Ixa9SCcK4daNPkWw77LpxLZl',
            'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp',
            'Host': host_url,
            'Referer': 'http://q.10jqka.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', },
            {'Accept': 'text/html, */*; q=0.01',
             'Accept-Encoding': 'gzip, deflate, sdch',
             'Accept-Language': 'zh-CN,zh;q=0.8',
             'Connection': 'keep-alive',
             'Cookie': 'user=MDq62tH9NUU6Ok5vbmU6NTAwOjQ2OTU0MjA4MDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQyMDgwOjE1MzM5OTg4OTc6OjoxNTMzOTk4ODgwOjg2NDAwOjA6MTEwOTNhMzBkNTAxMWFlOTg0OWM1MzVjODA2NjQyMThmOmRlZmF1bHRfMjox; userid=459542080; u_name=%BA%DA%D1%FD5E; escapename=%25u9ed1%25u59965E; ticket=658289e5730da881ef99b521b65da6af; log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469,1533998895,1533998953; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998953; v=AibgksC3Qd-feBV7t0kbK7PCd5e-B2rBPEueJRDPEskkk8xLeJe60Qzb7jDj',
             'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp',
             'Host': host_url,
             'Referer': 'http://q.10jqka.com.cn/',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
             },
            {'Accept': 'text/html, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, sdch',
             'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive',
             'Cookie': 'user=MDq62sm9wM%2FR%2FVk6Ok5vbmU6NTAwOjQ2OTU0MTY4MTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Ojo6NDU5NTQxNjgxOjE1MzM5OTg0NjI6OjoxNTMzOTk4NDYwOjg2NDAwOjA6MTAwNjE5YWExNjc2NDQ2MGE3ZGYxYjgxNDZlNzY3ODIwOmRlZmF1bHRfMjox; userid=459541681; u_name=%BA%DA%C9%BD%C0%CF%D1%FDY; escapename=%25u9ed1%25u5c71%25u8001%25u5996Y; ticket=4def626a5a60cc1d998231d7730d2947; log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361,1533998469; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533998496; v=AvYwAjBHsS9PCEXLZexL20PSRyfuFzpQjFtutWDf4ll0o5zbyKeKYVzrvsAz',
             'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp', 'Host': host_url,
             'Referer': 'http://q.10jqka.com.cn/',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
             'X-Requested-With': 'XMLHttpRequest'},
            {'Accept': 'text/html, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, sdch',
             'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive',
             'Cookie': 'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1533992361; user=MDq62sm9SnpsOjpOb25lOjUwMDo0Njk1NDE0MTM6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjo6OjQ1OTU0MTQxMzoxNTMzOTk4MjA5Ojo6MTUzMzk5ODE2MDo4NjQwMDowOjFlYTE2YTBjYTU4MGNmYmJlZWJmZWExODQ3ODRjOTAxNDpkZWZhdWx0XzI6MQ%3D%3D; userid=459541413; u_name=%BA%DA%C9%BDJzl; escapename=%25u9ed1%25u5c71Jzl; ticket=b909a4542156f3781a86b8aaefce3007; v=ApheKMKxdxX9FluRdtjNUdGcac08gfwLXuXQj9KJ5FOGbTKxepHMm671oBoh',
             'hexin-v': 'AiDRI3i0b1qEZNNemO_FOZlE8SXqKQQBpg9Y4Jox7pbOH8oZQjnUg_YdKIHp', 'Host': host_url,
             'Referer': 'http://q.10jqka.com.cn/',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
             'X-Requested-With': 'XMLHttpRequest'},
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': '__utma=156575163.1722582602.1604584020.1604584020.1604584020.1; __utmc=156575163; __utmz=156575163.1604584020.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; reviewJump=nojump; searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1604584201,1605188326,1605188771,1605190529; user=MDptb180ODg0NzI1MDI6Ok5vbmU6NTAwOjQ5ODQ3MjUwMjo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNDo6OjQ4ODQ3MjUwMjoxNjA1MTkwOTE5Ojo6MTU1ODY5ODk2MDo2MDQ4MDA6MDoxMDM3NTE4MjVkNGUwNjAzOGI0OTQyYWY3MTI2NDlmNGE6ZGVmYXVsdF80OjE%3D; userid=488472502; u_name=mo_488472502; escapename=mo_488472502; ticket=c00c8bcede8ce14379910ff82a559879; user_status=0; historystock=399001%7C*%7C399301%7C*%7C000571%7C*%7C399300; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1605192430; usersurvey=1; v=AqhQTrCHY-R1Pk9g_KZ5covaf5250Qzb7jXgX2LZ9CMWvUaLCuHcaz5FsO6x',
            'Host': host_url,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'},
        ]

        try:
            time.sleep(random()*2)
            # headers = choice(headers_list)
            headers = headers_list[-1]
            rp = requests.get(url=url, headers=headers, timeout=4)
            return rp.content
        except Exception as e:
            print(e)
            if num_retries > 0:
                print('重新下载')
                self.proxy_save = {}
                return self.downloader(url, num_retries - 1)
            else:
                if url not in FAILURE_URL_LIST:
                    FAILURE_URL_LIST.append(url)

    def code_msg_url_list(self):
        """
        组合请求的URL列表
        :return: 组合后的URL列表
        """
        url_list = []
        url = 'http://q.10jqka.com.cn/zs/detail/field/199112/order/desc/page/1/ajax/1/code/399300'
        html = self.downloader(url)
        bs = BeautifulSoup(html, 'html.parser')
        # 先获取当前url的最大页数
        max_page = bs.find(id='m-page').find_all('a')[-1]['page']
        for i in range(int(max_page)):
            url = '{}{}{}'.format('http://q.10jqka.com.cn/zs/detail/field/199112/order/desc/page/', i+1, '/ajax/1/code/399300')
            url_list.append(url)
        return url_list

    def code_msg(self):
        """
        获得沪深300的股票代码和现价，把包含index、代码、名称、现价数据写入csv文件
        :return:
        """
        url_list = self.code_msg_url_list()
        msg_list = []
        for url in url_list:
            try:
                html = self.downloader(url)
                bs = BeautifulSoup(html, 'html.parser')
                tr_list = bs.find('tbody').find_all('tr')
                for tr in tr_list:
                    # 列表包含数据index、代码、名称、现价
                    code_list = []
                    td_list = tr.find_all('td')
                    # items['index'] = td_list[0].string
                    # items['代码'] = td_list[1].string
                    # items['名称'] = td_list[2].string
                    # items['现价'] = td_list[3].string
                    code_list.append(td_list[0].string)
                    code_list.append(td_list[1].string)
                    code_list.append(td_list[2].string)
                    code_list.append(td_list[3].string)
                    msg_list.append(code_list)
            except:
                print(url)
        self.write_msg(msg_list, './stock_msg.csv')

    def write_msg(self, data, file_path):
        """
        把数据写入csv文件
        :param data: 写入的数据列表， 例如[['682','600426','华鲁恒升','34.30'], ['683','000423','东阿阿胶','41.55']]
        :param file_path: 保存的文件路径
        :return:
        """
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            for l in data:
                writer.writerow(l)

    def get_finance(self, code):
        """
        获取季度每股平均收益
        :param code: 股票代码
        :return:
        """
        url = 'http://basic.10jqka.com.cn/{}/finance.html'.format(code)
        try:
            rp = self.downloader(url)
            soup = BeautifulSoup(rp, 'html.parser')
            data_json = soup.find(id='main').text
            data_dict = json.loads(data_json)
            # 前四季度每股平均收益
            per_income_list = data_dict['simple'][7][0:4]
            return per_income_list
        except Exception as e:
            print(e)
            print('error finance url: {}'.format(url))

    def get_bonus(self, code):
        url = 'http://basic.10jqka.com.cn/{}/bonus.html'.format(code)
        try:
            rp = self.downloader(url)
            soup = BeautifulSoup(rp, 'html.parser')
            tr_list = soup.find('tbody').find_all('tr')
            for tr in tr_list:
                profit_list = []
                td_list = tr.find_all('td')
                profit_list.append(td_list[0].string)
                profit_list.append(td_list[1].string)
                profit_list.append(td_list[4].string)
                if profit_list[2] == '不分配不转增':
                    continue
                print(profit_list)
        except Exception as e:
            print(e)
            print('error bonus url: {}'.format(url))

if __name__ == '__main__':
    az = AnalyzeStock()
    AnalyzeStock().get_bonus('000963')
    # code_msg_url_list()
    # print(FAILURE_URL_LIST)
    # rd = az.downloader('https://mail.163.com/')
    # print(rd)



