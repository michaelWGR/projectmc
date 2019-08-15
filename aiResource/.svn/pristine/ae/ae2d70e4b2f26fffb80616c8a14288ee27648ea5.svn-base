# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest
import os
from management.third_party.aliyun import Aliyun
from management.third_party.baiducloud import BaiduCloud
from management.third_party.tuputech import TuPuCheck
from management.third_party.txcloud import TXCloud

__author__ = 'LibX'


# python -m unittest management.test.third_party

class TestAliyun(unittest.TestCase):
    def setUp(self):
        self.aliyun_instance = Aliyun("LTAIcMmmTfSs7rrH", "MV0tDj5rAr6Y0gWFTDwMl1orViOVyn", "green.cn-shanghai.aliyuncs.com",
               "cn-shanghai")
        self.porn_image_urls = [
        "http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg", ]
        self.orc_image_url = 'http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg'

    def test_porn_image(self):
        for image_url in self.porn_image_urls:
            result = self.aliyun_instance.porn_image(image_url)
            self.assertTrue(result)

    def test_ocr_image(self):
        result = self.aliyun_instance.ocr_image(self.orc_image_url)
        self.assertTrue(result)


class TestBaiduCloud(unittest.TestCase):
    def setUp(self):
        self.BaiduCloud_instance = BaiduCloud("11612348", "8wQ9G53im8RgZTebibkLsLg6", "YHrtk3LBbqox5TMQjCCwkCr31XnhjpHv")
        self.ocr_image_url = 'http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg'

    def test_ocr_image(self):
        result = self.BaiduCloud_instance.ocr_image(self.ocr_image_url)
        self.assertTrue(result)


class TestTupuTech(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pem_path = os.path.join(base_dir, "third_party", "pem")
        pem_file = os.path.join(pem_path, 'tupu_rsa_private_key.pem')
        secret_id = {"porn": '5b582d8393c70fabecff93a7', "ocr": '5b5aca05878b01abf107e3c9'}
        self.TupuTech_instance = TuPuCheck(secret_id, pem_file)
        self.porn_image_urls = [
            "http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg", ]
        self.orc_image_url = 'http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg'

    def test_porn_image(self):
        for image_url in self.porn_image_urls:
            result = self.TupuTech_instance.porn_image(image_url)
            self.assertTrue(result)

    def test_ocr_image(self):
        result = self.TupuTech_instance.ocr_image(self.orc_image_url)
        self.assertTrue(result)


class TestTxCloud(unittest.TestCase):
    def setUp(self):
        self.txCloud_instance = TXCloud("1257170265", "AKIDBLTUN88KmFZizBeyb6Rj5gKbieRq9W1O", "Ut7B6DF6pMk2FPSK6lIetzwlQ8vrlaHr")
        self.porn_image_urls = [
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1532942286314&di=622cee57b2ef1eebe970b5de7b2bbba0&imgtype=0&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0105455608951732f875a132b93e14.jpg%401280w_1l_2o_100sh.jpg"
        ,
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1533537075&di=3b5bef3819af1ff5473779746c76c867&imgtype=jpg&er=1&src=http%3A%2F%2Fs9.sinaimg.cn%2Fmw690%2F005Llvbrty72z9HBtUI58%26amp%3B690",
        "https://pics.javcdn.pw/cover/6ovy_b.jpg", ]
        self.orc_image_url = 'http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg'

    def test_porn_image(self):
        for image_url in self.porn_image_urls:
            result = self.txCloud_instance.porn_image(image_url)
            self.assertTrue(result)

    def test_ocr_image(self):
        result = self.txCloud_instance.ocr_image(self.orc_image_url)
        self.assertTrue(result)


class TestYY(unittest.TestCase):
    def setUp(self):
        from management.third_party.yyaiimage import ThirdParty

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pem_path = os.path.join(base_dir, "third_party", "pem")
        pem_file = os.path.join(pem_path, 'yy_rsa_private_key.pem')
        secret_id = '91ffeffb337b20e743c588ff84e13711'

        self.third_party = ThirdParty(secret_id, pem_file)

    def test_porn_image(self):
        porn_image_urls = [
            "http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg",
        ]

        for image_url in porn_image_urls:
            result = self.third_party.porn_image(image_url)
            self.assertTrue(result)

    def test_ocr_image(self):
        orc_image_urls = [
            'http://122.13.200.245:7070/resource/debug_sample/adv_ocr/TB2372Jnr1YBuNjSszhXXcUsFXa_!!440562472_20180723213417.jpg'
        ]

        for image_url in orc_image_urls:
            result = self.third_party.ocr_image(image_url)
            self.assertTrue(result)
