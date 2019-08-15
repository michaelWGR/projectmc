# -*- coding:utf-8 -*-
import ConfigParser
import datetime
import json
import os
import uuid

'''
pip install aliyun-python-sdk-core==2.8.2
pip install -v aliyun-python-sdk-green==3.2.0
'''

from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import ImageSyncScanRequest

root = os.path.dirname(os.path.abspath(__file__))


class AliyunScene(object):

    def __init__(self):
        cf = ConfigParser.ConfigParser()
        config_path = os.path.join(root, "aliyun.conf")
        cf.read(config_path)
        self.__clt = client.AcsClient(cf.get("config", "accessKeyId"), cf.get("config", "accessKeySecret"),
                                      cf.get("config", "server"))
        region_provider.modify_point('Green', cf.get("config", "server"), cf.get("config", "domain"))
        # 场景参数支持：porn（色情）、terrorism（暴恐）qrcode（二维码）、ad（图片广告）、ocr（文字识别）
        self.__scene = "porn"

    # def set_scene(self, scene_name):
    #     self.__scene = scene_name

    def sync_check(self, image_url):
        check_success = False
        request = ImageSyncScanRequest.ImageSyncScanRequest()
        request.set_accept_format('JSON')
        task = {"dataId": str(uuid.uuid1()),
                "url": image_url,
                "time": datetime.datetime.now().microsecond
                }

        request.set_content(bytearray(json.dumps({"tasks": [task], "scenes": [self.__scene]}), "utf-8"))
        response = self.__clt.do_action_with_exception(request)
        result = json.loads(response)
        if 200 == result["code"]:
            task_results = result["data"]
            for taskResult in task_results:
                if 200 == taskResult["code"]:
                    scene_results = taskResult["results"]
                    for sceneResult in scene_results:
                        suggestion = sceneResult["suggestion"]
                        check_success = True
                        return check_success, suggestion
                else:
                    return check_success, taskResult["msg"]
        else:
            return check_success, result["msg"]


if __name__ == "__main__":
    a = AliyunScene()
    plist = [
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1532942286314&di=622cee57b2ef1eebe970b5de7b2bbba0&imgtype=0&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0105455608951732f875a132b93e14.jpg%401280w_1l_2o_100sh.jpg"
        ,
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1533537075&di=3b5bef3819af1ff5473779746c76c867&imgtype=jpg&er=1&src=http%3A%2F%2Fs9.sinaimg.cn%2Fmw690%2F005Llvbrty72z9HBtUI58%26amp%3B690",
        "https://pics.javcdn.pw/cover/6ovy_b.jpg", ]
    for item in plist:
        print a.sync_check(item)
